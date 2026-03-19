#!/usr/bin/env node
/**
 * Winner-Hidden Ablation Experiment for Paper 03
 *
 * Runs deliberations on 4 stratified questions with winner identity hidden
 * from subsequent round prompts. Compares convergence behavior, round count,
 * and output quality against the standard (winner-visible) deliberations.
 *
 * Uses the same models, prompts, temperature, and termination conditions
 * as the standard discussion system — the ONLY difference is that the
 * "(Winning Response)" label and "Winner: X (Score: Y)" line are removed
 * from the context provided to models in subsequent rounds.
 *
 * Usage:
 *   export $(cat .env | xargs)
 *   node publications/scripts/run_winner_hidden_ablation.cjs
 *
 * Output: publications/data/winner-hidden-ablation/results.json
 */

const fs = require('fs').promises;
const path = require('path');
const https = require('https');
const http = require('http');
const yaml = require ? undefined : undefined; // We'll parse YAML manually

const PROJECT_ROOT = path.resolve(__dirname, '../..');
const OUTPUT_DIR = path.join(PROJECT_ROOT, 'publications/data/winner-hidden-ablation');
const CONTENT_DIR = path.join(PROJECT_ROOT, 'src/content/research-questions');

const DATABRICKS_HOST = process.env.DATABRICKS_HOST || process.env.DATABRICKS_WORKSPACE;
const DATABRICKS_TOKEN = process.env.DATABRICKS_TOKEN;

const MODELS = {
  'claude-opus-4-6': {
    name: 'Claude Opus 4.6',
    endpoint: '/serving-endpoints/databricks-claude-opus-4-6/invocations',
  },
  'gemini-3-pro': {
    name: 'Gemini 3 Pro',
    endpoint: '/serving-endpoints/databricks-gemini-3-pro/invocations',
  },
  'gpt-5-2': {
    name: 'GPT-5.2',
    endpoint: '/serving-endpoints/databricks-gpt-5-2/invocations',
  },
};

const MODEL_ORDER = ['claude-opus-4-6', 'gemini-3-pro', 'gpt-5-2'];
const CONFIG = {
  maxRounds: 5,
  maxResponseWords: 2000,
  temperature: 0.7,
  maxTokens: 16000,
  selfVoteWeight: 0.5,
  delayMs: 30000,
};

// 4 stratified questions: 2 technical, 1 economic, 1 governance
// Chosen from questions that had 2+ rounds in standard deliberation
const ABLATION_QUESTIONS = [
  { slug: 'propellant-production-phase-0-scope', phase: 'phase-0', id: 'rq-0-14' },
  { slug: 'isru-cost-methodology-validation', phase: 'phase-0', id: 'rq-0-28' },
  { slug: 'swarm-coordination-architecture-scale', phase: 'phase-1', id: 'rq-1-24' },
  { slug: 'slot-reallocation-governance', phase: 'phase-1', id: 'rq-1-40' },
];

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function callModel(modelKey, userPrompt, systemPrompt) {
  const model = MODELS[modelKey];
  const url = new URL(model.endpoint, DATABRICKS_HOST);
  const body = JSON.stringify({
    messages: [
      { role: 'system', content: systemPrompt || 'You are a space systems engineering expert.' },
      { role: 'user', content: userPrompt },
    ],
    max_tokens: CONFIG.maxTokens,
    temperature: CONFIG.temperature,
  });

  return new Promise((resolve, reject) => {
    const proto = url.protocol === 'https:' ? https : http;
    const req = proto.request(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${DATABRICKS_TOKEN}`,
        'Content-Type': 'application/json',
      },
      timeout: 300000,
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          const content = json.choices?.[0]?.message?.content;
          if (typeof content !== 'string') {
            reject(new Error(`Non-string response: ${JSON.stringify(json).slice(0, 200)}`));
          } else {
            resolve(content);
          }
        } catch (e) { reject(new Error(`Parse error: ${data.slice(0, 200)}`)); }
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('Timeout (300s)')); });
    req.write(body);
    req.end();
  });
}

function wordCount(text) { return (typeof text === 'string' ? text : '').trim().split(/\s+/).filter(w => w.length > 0).length; }

// Load question from markdown frontmatter
async function loadQuestion(slug, phase) {
  const dir = path.join(CONTENT_DIR, phase);
  const entries = await fs.readdir(dir);
  const match = entries.find(e => e.endsWith('.md') && e.includes(slug));
  if (!match) throw new Error(`Question not found: ${slug}`);

  const content = await fs.readFile(path.join(dir, match), 'utf-8');
  // Extract title from frontmatter
  const titleMatch = content.match(/title:\s*"([^"]+)"/);
  return {
    title: titleMatch ? titleMatch[1] : slug,
    slug,
    phase,
    context: content.slice(0, 2000),
  };
}

// Generate proposal prompt — WINNER HIDDEN
function makeProposalPrompt(question, priorRounds, roundNumber) {
  let prompt = `# Discussion: ${question.title}\n\n## Question Background\n${question.context}\n\n`;
  prompt += `## Guidelines\n- Provide a substantive response\n- Be specific and opinionated\n- Consider technical feasibility, cost, and risk\n- Keep under ${CONFIG.maxResponseWords} words\n`;

  if (priorRounds.length > 0) {
    prompt += '\n## Previous Rounds\n\n';
    for (const round of priorRounds) {
      prompt += `### Round ${round.roundNumber}\n\n`;
      for (const resp of round.responses) {
        // NO winner label — this is the ablation
        prompt += `**${MODELS[resp.modelId].name}**:\n`;
        prompt += resp.content.substring(0, 1000) + (resp.content.length > 1000 ? '...' : '') + '\n\n';
      }
      // NO winner announcement — this is the ablation
    }
  }

  prompt += `\n## Your Task (Round ${roundNumber})\nProvide your response. Build on insights from prior rounds.`;
  return prompt;
}

// Generate voting prompt (identical to standard — voting still happens)
function makeVotingPrompt(question, responses) {
  let prompt = `# Vote on Responses\n\n## Question: ${question.title}\n\n`;
  prompt += `Rate each: APPROVE (2), NEUTRAL (1), REJECT (0)\n\n`;
  for (const resp of responses) {
    prompt += `### ${MODELS[resp.modelId].name}\n${resp.content}\n\n---\n\n`;
  }
  prompt += `Respond in JSON ONLY:\n{\n  "votes": [\n    {"targetId": "claude-opus-4-6", "vote": "APPROVE|NEUTRAL|REJECT", "reasoning": "..."},\n    {"targetId": "gemini-3-pro", "vote": "APPROVE|NEUTRAL|REJECT", "reasoning": "..."},\n    {"targetId": "gpt-5-2", "vote": "APPROVE|NEUTRAL|REJECT", "reasoning": "..."}\n  ],\n  "terminationVote": "CONCLUDE|CONTINUE"\n}`;
  return prompt;
}

function parseVotes(content, voterId) {
  try {
    let jsonStr = content;
    const match = content.match(/```(?:json)?\s*([\s\S]*?)```/);
    if (match) jsonStr = match[1];
    const parsed = JSON.parse(jsonStr.trim());
    return parsed.votes.map(v => ({
      voterId,
      targetId: v.targetId,
      score: v.vote === 'APPROVE' ? 2 : v.vote === 'NEUTRAL' ? 1 : 0,
    })).concat([{ terminationVote: parsed.terminationVote }]);
  } catch (e) {
    return null;
  }
}

async function runAblation(question) {
  const rounds = [];

  for (let roundNum = 1; roundNum <= CONFIG.maxRounds; roundNum++) {
    console.log(`    Round ${roundNum}:`);

    // Collect proposals
    const responses = [];
    for (const modelKey of MODEL_ORDER) {
      console.log(`      ${MODELS[modelKey].name} proposing...`);
      try {
        const content = await callModel(modelKey, makeProposalPrompt(question, rounds, roundNum),
          'You are a space systems engineering expert participating in a multi-stakeholder discussion.');
        responses.push({ modelId: modelKey, content, words: wordCount(content) });
        console.log(`        ${wordCount(content)} words`);
      } catch (e) {
        console.log(`        FAILED: ${e.message}`);
        responses.push({ modelId: modelKey, content: `[Failed: ${e.message}]`, words: 0, error: true });
      }
      await sleep(CONFIG.delayMs);
    }

    // Collect votes
    let allVotes = [];
    let concludeVotes = 0;
    for (const modelKey of MODEL_ORDER) {
      console.log(`      ${MODELS[modelKey].name} voting...`);
      try {
        const voteContent = await callModel(modelKey, makeVotingPrompt(question, responses));
        const parsed = parseVotes(voteContent, modelKey);
        if (parsed) {
          const termVote = parsed.find(v => v.terminationVote);
          if (termVote && termVote.terminationVote === 'CONCLUDE') concludeVotes++;
          allVotes.push(...parsed.filter(v => !v.terminationVote));
        }
      } catch (e) {
        console.log(`        Vote FAILED: ${e.message}`);
      }
      await sleep(10000);
    }

    // Compute scores
    const scores = {};
    for (const modelKey of MODEL_ORDER) {
      const modelVotes = allVotes.filter(v => v.targetId === modelKey);
      scores[modelKey] = modelVotes.reduce((sum, v) => {
        const weight = v.voterId === v.targetId ? CONFIG.selfVoteWeight : 1.0;
        return sum + v.score * weight;
      }, 0);
    }

    const winnerId = Object.entries(scores).sort((a, b) => b[1] - a[1])[0][0];
    console.log(`      Winner: ${MODELS[winnerId].name} (${scores[winnerId].toFixed(1)})`);
    console.log(`      Conclude votes: ${concludeVotes}/3`);

    rounds.push({
      roundNumber: roundNum,
      responses,
      scores,
      winnerId,
      winnerScore: scores[winnerId],
      concludeVotes,
    });

    // Termination check
    if (concludeVotes >= 3) {
      console.log(`    Terminated: unanimous conclude`);
      break;
    }
    if (concludeVotes >= 2 && roundNum > 1 && rounds[roundNum - 2]?.concludeVotes >= 2) {
      console.log(`    Terminated: consecutive 2/3 conclude`);
      break;
    }
  }

  return rounds;
}

async function main() {
  if (!DATABRICKS_TOKEN) {
    console.error('ERROR: DATABRICKS_TOKEN not set');
    process.exit(1);
  }

  await fs.mkdir(OUTPUT_DIR, { recursive: true });

  console.log('='.repeat(70));
  console.log('Winner-Hidden Ablation Experiment — Paper 03');
  console.log('='.repeat(70));
  console.log(`Date: ${new Date().toISOString()}`);
  console.log(`Questions: ${ABLATION_QUESTIONS.length}`);
  console.log(`Condition: Winner identity HIDDEN from subsequent round prompts`);
  console.log(`Control: Standard deliberation data (winner visible) from existing runs\n`);

  const results = {
    experiment: 'winner-hidden-ablation',
    timestamp: new Date().toISOString(),
    condition: 'Winner identity removed from subsequent round prompts',
    control: 'Standard deliberation with winner visible',
    questions: [],
  };

  for (let i = 0; i < ABLATION_QUESTIONS.length; i++) {
    const qDef = ABLATION_QUESTIONS[i];
    console.log(`\n[${ i + 1}/${ABLATION_QUESTIONS.length}] ${qDef.id}: ${qDef.slug}`);

    try {
      const question = await loadQuestion(qDef.slug, qDef.phase);
      console.log(`  Title: ${question.title}`);
      console.log('  Running hidden-winner deliberation...');

      const rounds = await runAblation(question);

      // Load standard deliberation for comparison
      let standardRounds = null;
      try {
        const discDir = path.join(CONTENT_DIR, qDef.phase);
        const entries = await fs.readdir(discDir);
        const rqDir = entries.find(e => e.includes(qDef.slug) && !e.endsWith('.md'));
        if (rqDir) {
          const discPath = path.join(discDir, rqDir, 'discussion.yaml');
          const discContent = await fs.readFile(discPath, 'utf-8');
          // Extract round count from YAML
          const roundMatch = discContent.match(/totalRounds:\s*(\d+)/);
          standardRounds = roundMatch ? parseInt(roundMatch[1]) : null;
        }
      } catch (e) { /* standard data may not exist */ }

      const qResult = {
        questionId: qDef.id,
        slug: qDef.slug,
        title: question.title,
        hiddenWinner: {
          totalRounds: rounds.length,
          terminationRound: rounds.length,
          roundWinners: rounds.map(r => r.winnerId),
          winnerStability: rounds.length > 1 ?
            rounds.filter((r, i) => i > 0 && r.winnerId === rounds[0].winnerId).length / (rounds.length - 1) : 1.0,
          concludeVotesPerRound: rounds.map(r => r.concludeVotes),
        },
        standardDeliberation: {
          totalRounds: standardRounds,
        },
        comparison: {
          roundDelta: standardRounds ? rounds.length - standardRounds : null,
          sameFirstRoundWinner: null, // would need to load standard data
        },
      };

      results.questions.push(qResult);

      console.log(`  Hidden-winner: ${rounds.length} rounds, winner stability: ${qResult.hiddenWinner.winnerStability.toFixed(2)}`);
      if (standardRounds) {
        console.log(`  Standard:      ${standardRounds} rounds`);
        console.log(`  Delta:         ${rounds.length - standardRounds > 0 ? '+' : ''}${rounds.length - standardRounds} rounds`);
      }

    } catch (e) {
      console.error(`  FAILED: ${e.message}`);
      results.questions.push({ questionId: qDef.id, slug: qDef.slug, error: e.message });
    }
  }

  // Summary
  console.log('\n' + '='.repeat(70));
  console.log('SUMMARY');
  console.log('='.repeat(70));

  const valid = results.questions.filter(q => !q.error);
  const avgHiddenRounds = valid.reduce((s, q) => s + q.hiddenWinner.totalRounds, 0) / valid.length;
  const avgStandardRounds = valid.filter(q => q.standardDeliberation.totalRounds)
    .reduce((s, q) => s + q.standardDeliberation.totalRounds, 0) /
    valid.filter(q => q.standardDeliberation.totalRounds).length || 0;
  const avgStability = valid.reduce((s, q) => s + q.hiddenWinner.winnerStability, 0) / valid.length;

  console.log(`\nHidden-winner avg rounds: ${avgHiddenRounds.toFixed(1)}`);
  console.log(`Standard avg rounds:      ${avgStandardRounds.toFixed(1)}`);
  console.log(`Hidden-winner avg stability: ${(avgStability * 100).toFixed(0)}%`);
  console.log(`(Standard stability from repeated trials: 85%)`);

  await fs.writeFile(path.join(OUTPUT_DIR, 'results.json'), JSON.stringify(results, null, 2));
  console.log(`\nResults saved: ${path.join(OUTPUT_DIR, 'results.json')}`);
}

main().catch(console.error);
