#!/usr/bin/env node
/**
 * Controlled Baseline Experiments for Paper 03 (Multi-Model AI Consensus)
 *
 * PROMPT-MATCHED baselines addressing reviewer demands (Claude, Gemini, GPT all
 * require controlled comparisons before publication).
 *
 * Two experiments:
 *   Exp 1 — Aggregation-only: All 3 models produce Round 1 proposals using the
 *           EXACT same prompt as deliberation, then a single synthesis aggregates.
 *           No voting, no rounds. Tests whether deliberation adds value over simple
 *           multi-model aggregation.
 *
 *   Exp 2 — Self-refinement: Each of 3 models generates a Round 1 proposal,
 *           then self-critiques and refines for the same number of rounds as
 *           deliberation took. Tests whether cross-model feedback matters vs.
 *           single-model self-improvement.
 *
 * Key design constraints (prompt-matching):
 *   - Round 1 prompt is IDENTICAL to run-discussion.js generateResponsePrompt()
 *   - Synthesis prompt matches generateConclusion() structure
 *   - Same temperature (0.7), same max_tokens (16000 proposals, 8000 synthesis)
 *   - Same models: Claude Opus 4.6, Gemini 3 Pro, GPT-5.2
 *
 * Usage:
 *   export $(cat .env | xargs)
 *   node publications/scripts/run_controlled_baselines.cjs
 *   node publications/scripts/run_controlled_baselines.cjs --exp=1   # aggregation-only
 *   node publications/scripts/run_controlled_baselines.cjs --exp=2   # self-refinement
 *   node publications/scripts/run_controlled_baselines.cjs --question=rq-0-14  # single question
 *
 * Output: publications/data/controlled-baselines/results.json
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// =============================================================================
// HYPERPARAMETERS — All captured explicitly for reproducibility
// =============================================================================
const HYPERPARAMS = {
  // API Configuration
  databricksHost: process.env.DATABRICKS_HOST || process.env.DATABRICKS_WORKSPACE || 'https://adb-6239133969168510.10.azuredatabricks.net',
  models: {
    'claude-opus-4-6': {
      id: 'databricks-claude-opus-4-6',
      name: 'Claude Opus 4.6',
      endpoint: '/serving-endpoints/databricks-claude-opus-4-6/invocations',
    },
    'gemini-3-pro': {
      id: 'databricks-gemini-3-pro',
      name: 'Gemini 3 Pro',
      endpoint: '/serving-endpoints/databricks-gemini-3-pro/invocations',
    },
    'gpt-5-2': {
      id: 'databricks-gpt-5-2',
      name: 'GPT-5.2',
      endpoint: '/serving-endpoints/databricks-gpt-5-2/invocations',
    },
  },
  modelOrder: ['claude-opus-4-6', 'gemini-3-pro', 'gpt-5-2'],

  // Generation parameters — MATCHED to deliberation (run-discussion.js)
  proposalMaxTokens: 16000,     // Same as deliberation responses
  proposalTemperature: 0.7,     // Same as deliberation
  synthesisMaxTokens: 8000,     // Same as deliberation conclusion
  synthesisTemperature: 0.7,    // Deliberation conclusion uses 0.7 (via queryDatabricks default)
  maxResponseWords: 2000,       // Same word limit in prompt

  // Synthesis model — MATCHED to deliberation (always Claude)
  synthesisModel: 'claude-opus-4-6',
  synthesisSystemPrompt: 'You are synthesizing a multi-model discussion into actionable conclusions.',

  // Rate limiting
  delayBetweenCallsMs: 30000,   // 30s between API calls to avoid rate limits
  delayBetweenQuestionsMs: 10000, // 10s between questions

  // Experiment metadata
  scriptVersion: '1.0.0',
  scriptPath: 'publications/scripts/run_controlled_baselines.cjs',
  deliberationScriptRef: 'scripts/run-discussion.js',
  promptMatchingNotes: [
    'Round 1 prompt is identical to generateResponsePrompt() in run-discussion.js',
    'No system prompt for proposals (matching deliberation which uses user-prompt-only)',
    'Synthesis prompt matches generateConclusion() structure and system prompt',
    'Temperature and max_tokens match deliberation exactly',
    'All 3 models used (not just Claude as in prior self-refinement baseline)',
    'Self-refinement prompt provides own prior response (not other models responses)',
  ],
};

// =============================================================================
// QUESTION DEFINITIONS — All 16 deliberation questions with metadata
// =============================================================================
const BASE_DIR = path.join(__dirname, '..', '..', 'src', 'content', 'research-questions');
const OUTPUT_DIR = path.join(__dirname, '..', 'data', 'controlled-baselines');

const QUESTIONS = [
  { id: 'rq-0-14', slug: 'rq-0-14-propellant-production-phase-0-scope', phase: 'phase-0', title: 'Propellant production in Phase 0 scope', deliberationRounds: 1, category: 'technical-systems' },
  { id: 'rq-0-18', slug: 'rq-0-18-human-rating-transport-vehicles', phase: 'phase-0', title: 'Human-rating requirement for transport vehicles', deliberationRounds: 1, category: 'technical-systems' },
  { id: 'rq-0-26', slug: 'rq-0-26-dual-bucket-wheel-excavation', phase: 'phase-0', title: 'Dual counter-rotating bucket-wheel excavation for microgravity torque balancing', deliberationRounds: 1, category: 'technical-systems' },
  { id: 'rq-0-28', slug: 'rq-0-28-isru-cost-methodology-validation', phase: 'phase-0', title: 'In-situ resource utilization cost methodology validation', deliberationRounds: 3, category: 'economic-methodology' },
  { id: 'rq-0-29', slug: 'rq-0-29-multi-century-governance-structure', phase: 'phase-0', title: 'Governance structure for multi-century, volunteer-driven global coordination', deliberationRounds: 1, category: 'governance' },
  { id: 'rq-1-11', slug: 'rq-1-11-swarm-power-architecture-end-use', phase: 'phase-1', title: 'Swarm-level power architecture and end-use', deliberationRounds: 1, category: 'technical-systems' },
  { id: 'rq-1-16', slug: 'rq-1-16-autonomous-assembly-certification', phase: 'phase-1', title: 'Autonomy certification for fully autonomous assembly', deliberationRounds: 1, category: 'technical-systems' },
  { id: 'rq-1-21', slug: 'rq-1-21-feedstock-acquisition-isru-timeline', phase: 'phase-1', title: 'Feedstock acquisition and ISRU transition timeline', deliberationRounds: 1, category: 'technical-systems' },
  { id: 'rq-1-24', slug: 'rq-1-24-swarm-coordination-architecture-scale', phase: 'phase-1', title: 'Swarm coordination architecture at scale (millions of units)', deliberationRounds: 2, category: 'technical-systems' },
  { id: 'rq-1-33', slug: 'rq-1-33-tug-end-of-life-disposal', phase: 'phase-1', title: 'End-of-life disposal protocol for orbital tugs', deliberationRounds: 1, category: 'technical-systems' },
  { id: 'rq-1-40', slug: 'rq-1-40-slot-reallocation-governance', phase: 'phase-1', title: 'Slot reallocation governance protocol', deliberationRounds: 2, category: 'governance' },
  { id: 'rq-1-42', slug: 'rq-1-42-node-end-of-life-disposal', phase: 'phase-1', title: 'End-of-life disposal for failed swarm nodes', deliberationRounds: 2, category: 'technical-systems' },
  { id: 'rq-2-17', slug: 'rq-2-17-fleet-coordination-scale-constraints', phase: 'phase-2', title: 'Fleet coordination constraints at scale', deliberationRounds: 2, category: 'technical-systems' },
  { id: 'rq-2-20', slug: 'rq-2-20-swarm-roi-threshold-humanity-power-needs', phase: 'phase-2', title: 'Swarm operational threshold for meeting humanity\'s energy needs', deliberationRounds: 2, category: 'economic-methodology' },
  { id: 'rq-2-3', slug: 'rq-2-3-billion-unit-collision-avoidance', phase: 'phase-2', title: 'Collision avoidance certification for billion-unit swarms', deliberationRounds: 1, category: 'technical-systems' },
  { id: 'rq-2-8', slug: 'rq-2-8-autonomous-repair-authority-limits', phase: 'phase-2', title: 'Autonomous repair authority limits', deliberationRounds: 1, category: 'governance' },
];

// =============================================================================
// API HELPERS
// =============================================================================

const DATABRICKS_TOKEN = process.env.DATABRICKS_TOKEN;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function stripFrontmatter(content) {
  const match = content.match(/^---\n[\s\S]*?\n---\n/);
  if (match) return content.slice(match[0].length).trim();
  return content.trim();
}

function wordCount(text) {
  return text.trim().split(/\s+/).filter(w => w.length > 0).length;
}

function callModel(modelKey, userPrompt, options = {}) {
  const { maxTokens = HYPERPARAMS.proposalMaxTokens, temperature = HYPERPARAMS.proposalTemperature, systemPrompt = null } = options;
  const model = HYPERPARAMS.models[modelKey];
  const apiUrl = `${HYPERPARAMS.databricksHost}${model.endpoint}`;

  return new Promise((resolve, reject) => {
    const url = new URL(apiUrl);
    const isHttps = url.protocol === 'https:';
    const lib = isHttps ? https : http;

    const messages = [];
    if (systemPrompt) messages.push({ role: 'system', content: systemPrompt });
    messages.push({ role: 'user', content: userPrompt });

    const body = JSON.stringify({ messages, max_tokens: maxTokens, temperature });

    const reqOpts = {
      hostname: url.hostname,
      port: url.port || (isHttps ? 443 : 80),
      path: url.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${DATABRICKS_TOKEN}`,
        'Content-Length': Buffer.byteLength(body),
      },
    };

    const req = lib.request(reqOpts, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            const parsed = JSON.parse(data);
            let text = parsed.choices?.[0]?.message?.content || '';
            // Gemini sometimes returns array content
            if (Array.isArray(text)) {
              text = text.filter(p => p.type === 'text').map(p => p.text).join('\n');
            }
            resolve(text);
          } catch (e) {
            reject(new Error(`JSON parse error for ${modelKey}: ${e.message}\nRaw: ${data.slice(0, 500)}`));
          }
        } else {
          reject(new Error(`API error ${res.statusCode} for ${modelKey}: ${data.slice(0, 500)}`));
        }
      });
    });

    req.on('error', reject);
    req.setTimeout(300000, () => {
      req.destroy();
      reject(new Error(`Request timeout (300s) for ${modelKey}`));
    });
    req.write(body);
    req.end();
  });
}

// =============================================================================
// PROMPT TEMPLATES — MATCHED to run-discussion.js
// =============================================================================

/**
 * Round 1 proposal prompt — IDENTICAL to generateResponsePrompt() in
 * run-discussion.js (lines 278-314) for roundNumber=1 with no prior rounds.
 */
function round1Prompt(question) {
  return `# Discussion: ${question.title}

## Question Background
${question.context}

## Discussion Guidelines
- Provide a substantive response addressing the research question
- Be specific and opinionated about recommended approaches
- Consider technical feasibility, cost implications, and risk factors
- Reference existing Project Dyson specifications where relevant
- Keep your response under ${HYPERPARAMS.maxResponseWords} words

## Your Task (Round 1)
Provide your response to the research question. Build on insights from prior rounds if applicable.`;
}

/**
 * Self-refinement prompt for Exp 2 — models critique their own prior response.
 * This is NOT in the deliberation system (which uses cross-model feedback instead).
 * The prompt structure parallels the deliberation Round N prompt but shows only
 * the model's own prior response (not other models').
 */
function selfRefinementPrompt(question, priorResponse, roundNumber) {
  return `# Discussion: ${question.title}

## Question Background
${question.context}

## Discussion Guidelines
- Provide a substantive response addressing the research question
- Be specific and opinionated about recommended approaches
- Consider technical feasibility, cost implications, and risk factors
- Reference existing Project Dyson specifications where relevant
- Keep your response under ${HYPERPARAMS.maxResponseWords} words

## Previous Round

### Round ${roundNumber - 1}

**Your previous response:**
${priorResponse.substring(0, 1000)}${priorResponse.length > 1000 ? '...' : ''}

## Your Task (Round ${roundNumber})
Critically review your previous response. Identify weaknesses, gaps, or alternative approaches you may have overlooked, and provide an improved response that addresses those issues. Build on your prior insights while strengthening the analysis.`;
}

/**
 * Aggregation-only synthesis prompt (Exp 1) — matches generateConclusion()
 * structure from run-discussion.js (lines 629-665), but fed Round 1 proposals
 * from all 3 models instead of multi-round discussion summaries.
 */
function aggregationSynthesisPrompt(question, proposals) {
  let context = `# Generate Discussion Conclusion

## Question: ${question.title}

## Question Background
${question.context}

## Proposals from Three Independent Models

`;

  for (const p of proposals) {
    const modelName = HYPERPARAMS.models[p.modelId].name;
    context += `### ${modelName}\n${p.content}\n\n---\n\n`;
  }

  context += `## Your Task

Synthesize the three proposals into a conclusion document with:

1. **Summary**: A 2-3 paragraph synthesis of the key conclusions
2. **Key Points**: 4-6 bullet points of main agreements
3. **Unresolved Questions**: 2-4 questions that remain open
4. **Recommended Actions**: 3-5 specific next steps

Format your response in markdown.`;

  return context;
}

/**
 * Self-refinement synthesis prompt (Exp 2) — same structure as above,
 * but uses a single model's final refined proposal.
 */
function selfRefinementSynthesisPrompt(question, finalProposal, modelId) {
  const modelName = HYPERPARAMS.models[modelId].name;
  return `# Generate Discussion Conclusion

## Question: ${question.title}

## Question Background
${question.context}

## Final Refined Proposal from ${modelName}

${finalProposal}

## Your Task

Synthesize the proposal into a conclusion document with:

1. **Summary**: A 2-3 paragraph synthesis of the key conclusions
2. **Key Points**: 4-6 bullet points of main agreements
3. **Unresolved Questions**: 2-4 questions that remain open
4. **Recommended Actions**: 3-5 specific next steps

Format your response in markdown.`;
}

// =============================================================================
// METRICS EXTRACTION (reused from self_refinement_baseline.cjs)
// =============================================================================

function isSectionHeader(line, patterns) {
  if (!/^#+\s+/.test(line)) return false;
  const headerText = line.replace(/^#+\s+/, '').replace(/^\d+[\.\):]?\s*/, '');
  return patterns.some(p => p.test(headerText));
}

function countSectionItems(text, sectionPatterns) {
  const lines = text.split('\n');
  let inSection = false;
  let sectionLevel = 0;
  let subHeadingCount = 0;
  let inlineCount = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;

    if (!inSection && isSectionHeader(line, sectionPatterns)) {
      inSection = true;
      sectionLevel = (line.match(/^#+/) || [''])[0].length;
      continue;
    }

    if (inSection && /^#+\s+/.test(line)) {
      const level = (line.match(/^#+/) || [''])[0].length;
      if (level <= sectionLevel) {
        const headerText = line.replace(/^#+\s+/, '').replace(/^\d+[\.\):]?\s*/, '');
        const stillInSection = sectionPatterns.some(p => p.test(headerText));
        if (!stillInSection) { inSection = false; continue; }
      }
      if (level > sectionLevel && line.length > 15) { subHeadingCount++; continue; }
    }

    if (inSection) {
      if (/^\d+[\.\)]\s+/.test(line) && line.length > 15) inlineCount++;
      else if (/^[-*]\s+\*\*/.test(line) && line.length > 15) inlineCount++;
    }
  }

  return subHeadingCount > 0 ? subHeadingCount : Math.max(inlineCount, 0);
}

function extractMetrics(text) {
  return {
    tradeoffs: countSectionItems(text, [/^trade[- ]?off/i, /^divergent/i, /^areas?\s+of\s+disagree/i]),
    keyPoints: countSectionItems(text, [/^key\s+point/i, /^key\s+findings/i, /^points?\s+of\s+agree/i]),
    unresolvedQuestions: countSectionItems(text, [/^unresolved/i, /^open\s+question/i, /^remaining/i]),
    recommendedActions: countSectionItems(text, [/^recommended\s+action/i, /^next\s+step/i, /^action\s+item/i]),
    wordCount: wordCount(text),
  };
}

// =============================================================================
// EXPERIMENT RUNNERS
// =============================================================================

async function runExperiment1(question) {
  console.log(`\n  --- Experiment 1: Aggregation-Only ---`);

  // Step 1: All 3 models produce Round 1 proposals
  const proposals = [];
  for (const modelKey of HYPERPARAMS.modelOrder) {
    const modelName = HYPERPARAMS.models[modelKey].name;
    console.log(`  [Exp1] ${modelName} generating proposal...`);
    const startTime = Date.now();

    try {
      const content = await callModel(modelKey, round1Prompt(question));
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
      console.log(`  [Exp1] ${modelName}: ${wordCount(content)} words, ${content.length} chars (${elapsed}s)`);
      proposals.push({
        modelId: modelKey,
        content,
        wordCount: wordCount(content),
        charCount: content.length,
        latencyMs: Date.now() - startTime,
      });
    } catch (err) {
      console.error(`  [Exp1] ${modelName} FAILED: ${err.message}`);
      proposals.push({ modelId: modelKey, error: err.message });
    }

    await sleep(HYPERPARAMS.delayBetweenCallsMs);
  }

  // Step 2: Single synthesis call (using Claude, matching deliberation)
  console.log(`  [Exp1] Generating aggregation synthesis...`);
  const validProposals = proposals.filter(p => !p.error);
  let synthesis = null;
  let synthesisMetrics = null;

  if (validProposals.length >= 2) {
    try {
      const synthContent = await callModel(
        HYPERPARAMS.synthesisModel,
        aggregationSynthesisPrompt(question, validProposals),
        {
          maxTokens: HYPERPARAMS.synthesisMaxTokens,
          temperature: HYPERPARAMS.synthesisTemperature,
          systemPrompt: HYPERPARAMS.synthesisSystemPrompt,
        }
      );
      synthesis = synthContent;
      synthesisMetrics = extractMetrics(synthContent);
      console.log(`  [Exp1] Synthesis: ${wordCount(synthContent)} words`);
    } catch (err) {
      console.error(`  [Exp1] Synthesis FAILED: ${err.message}`);
    }
  } else {
    console.log(`  [Exp1] Skipping synthesis (only ${validProposals.length} valid proposals)`);
  }

  return {
    experiment: 'aggregation-only',
    proposals,
    synthesis,
    synthesisMetrics,
    apiCalls: proposals.length + (synthesis ? 1 : 0),
  };
}

async function runExperiment2(question) {
  const totalRounds = question.deliberationRounds;
  console.log(`\n  --- Experiment 2: Self-Refinement (${totalRounds} rounds per model) ---`);

  const perModelResults = {};

  for (const modelKey of HYPERPARAMS.modelOrder) {
    const modelName = HYPERPARAMS.models[modelKey].name;
    console.log(`\n  [Exp2] ${modelName}: ${totalRounds} round(s)`);

    const rounds = [];
    let currentProposal = '';

    for (let round = 1; round <= totalRounds; round++) {
      const startTime = Date.now();

      try {
        let content;
        if (round === 1) {
          console.log(`    Round ${round}: generating proposal...`);
          content = await callModel(modelKey, round1Prompt(question));
        } else {
          console.log(`    Round ${round}: self-refining...`);
          content = await callModel(modelKey, selfRefinementPrompt(question, currentProposal, round));
        }

        const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
        console.log(`    Round ${round}: ${wordCount(content)} words (${elapsed}s)`);
        currentProposal = content;
        rounds.push({
          round,
          type: round === 1 ? 'initial' : 'self-refinement',
          content,
          wordCount: wordCount(content),
          charCount: content.length,
          latencyMs: Date.now() - startTime,
        });
      } catch (err) {
        console.error(`    Round ${round} FAILED: ${err.message}`);
        rounds.push({ round, error: err.message });
      }

      await sleep(HYPERPARAMS.delayBetweenCallsMs);
    }

    // Synthesis for this model
    let synthesis = null;
    let synthesisMetrics = null;
    if (currentProposal) {
      try {
        console.log(`    Generating synthesis for ${modelName}...`);
        const synthContent = await callModel(
          HYPERPARAMS.synthesisModel,
          selfRefinementSynthesisPrompt(question, currentProposal, modelKey),
          {
            maxTokens: HYPERPARAMS.synthesisMaxTokens,
            temperature: HYPERPARAMS.synthesisTemperature,
            systemPrompt: HYPERPARAMS.synthesisSystemPrompt,
          }
        );
        synthesis = synthContent;
        synthesisMetrics = extractMetrics(synthContent);
        console.log(`    Synthesis: ${wordCount(synthContent)} words`);
      } catch (err) {
        console.error(`    Synthesis FAILED: ${err.message}`);
      }
      await sleep(HYPERPARAMS.delayBetweenCallsMs);
    }

    perModelResults[modelKey] = {
      modelId: modelKey,
      rounds,
      synthesis,
      synthesisMetrics,
      apiCalls: rounds.length + (synthesis ? 1 : 0),
    };
  }

  return {
    experiment: 'self-refinement',
    roundsPerModel: totalRounds,
    perModelResults,
    apiCalls: Object.values(perModelResults).reduce((sum, r) => sum + r.apiCalls, 0),
  };
}

// =============================================================================
// MAIN
// =============================================================================

async function main() {
  if (!DATABRICKS_TOKEN) {
    console.error('ERROR: DATABRICKS_TOKEN not set.');
    console.error('Run: export $(cat /Users/hakketh/projects/experiments/dyson/.env | xargs)');
    process.exit(1);
  }

  // Parse CLI args
  const args = process.argv.slice(2).reduce((acc, arg) => {
    const [key, val] = arg.replace(/^--/, '').split('=');
    acc[key] = val || 'true';
    return acc;
  }, {});

  const runExp1 = !args.exp || args.exp === '1' || args.exp === 'both';
  const runExp2 = !args.exp || args.exp === '2' || args.exp === 'both';
  const questionFilter = args.question || null;

  const questions = questionFilter
    ? QUESTIONS.filter(q => q.id === questionFilter || q.slug.includes(questionFilter))
    : QUESTIONS;

  console.log('='.repeat(70));
  console.log('Controlled Baseline Experiments — Paper 03');
  console.log('='.repeat(70));
  console.log(`Script version: ${HYPERPARAMS.scriptVersion}`);
  console.log(`Date: ${new Date().toISOString()}`);
  console.log(`Experiments: ${runExp1 ? 'Exp1 (aggregation)' : ''} ${runExp2 ? 'Exp2 (self-refinement)' : ''}`);
  console.log(`Questions: ${questions.length} of ${QUESTIONS.length}`);
  console.log(`Models: ${HYPERPARAMS.modelOrder.join(', ')}`);
  console.log(`Proposal: T=${HYPERPARAMS.proposalTemperature}, max_tokens=${HYPERPARAMS.proposalMaxTokens}`);
  console.log(`Synthesis: T=${HYPERPARAMS.synthesisTemperature}, max_tokens=${HYPERPARAMS.synthesisMaxTokens}, model=${HYPERPARAMS.synthesisModel}`);
  console.log(`Delay between calls: ${HYPERPARAMS.delayBetweenCallsMs / 1000}s`);
  console.log();

  // Load existing results for resume support
  const outputPath = path.join(OUTPUT_DIR, 'results.json');
  let existingResults = {};
  if (fs.existsSync(outputPath)) {
    try {
      const saved = JSON.parse(fs.readFileSync(outputPath, 'utf-8'));
      existingResults = saved.questionResults || {};
      console.log(`Loaded ${Object.keys(existingResults).length} existing question results (resume mode)`);
    } catch (e) {
      console.log('Could not load existing results, starting fresh');
    }
  }

  const questionResults = { ...existingResults };
  let totalApiCalls = 0;
  const startTime = Date.now();

  for (let qi = 0; qi < questions.length; qi++) {
    const q = questions[qi];

    console.log(`\n${'='.repeat(70)}`);
    console.log(`[${qi + 1}/${questions.length}] ${q.id}: ${q.title}`);
    console.log(`  Phase: ${q.phase} | Deliberation rounds: ${q.deliberationRounds} | Category: ${q.category}`);
    console.log('='.repeat(70));

    // Read question context
    const mdPath = path.join(BASE_DIR, q.phase, `${q.slug}.md`);
    if (!fs.existsSync(mdPath)) {
      console.error(`  SKIPPED: question markdown not found at ${mdPath}`);
      continue;
    }
    const questionContext = stripFrontmatter(fs.readFileSync(mdPath, 'utf-8'));
    const questionObj = { ...q, context: questionContext };

    // Read deliberation conclusion for comparison
    const conclusionPath = path.join(BASE_DIR, q.phase, q.slug, 'conclusion.md');
    let deliberationConclusion = null;
    let deliberationMetrics = null;
    if (fs.existsSync(conclusionPath)) {
      deliberationConclusion = stripFrontmatter(fs.readFileSync(conclusionPath, 'utf-8'));
      deliberationMetrics = extractMetrics(deliberationConclusion);
    }

    const result = {
      questionId: q.id,
      questionSlug: q.slug,
      questionTitle: q.title,
      phase: q.phase,
      category: q.category,
      deliberationRounds: q.deliberationRounds,
      deliberationMetrics,
      timestamp: new Date().toISOString(),
    };

    // Check resume: skip if both experiments already done
    const existing = existingResults[q.id];
    const exp1Done = existing?.exp1 && !existing.exp1.error;
    const exp2Done = existing?.exp2 && !existing.exp2.error;

    // Experiment 1: Aggregation-only
    if (runExp1) {
      if (exp1Done) {
        console.log('  [Exp1] Already completed (resume mode), skipping');
        result.exp1 = existing.exp1;
      } else {
        result.exp1 = await runExperiment1(questionObj);
        totalApiCalls += result.exp1.apiCalls;
      }
    }

    // Experiment 2: Self-refinement
    if (runExp2) {
      if (exp2Done) {
        console.log('  [Exp2] Already completed (resume mode), skipping');
        result.exp2 = existing.exp2;
      } else {
        result.exp2 = await runExperiment2(questionObj);
        totalApiCalls += result.exp2.apiCalls;
      }
    }

    // Compute deltas
    if (deliberationMetrics) {
      if (result.exp1?.synthesisMetrics) {
        result.exp1.delta = {
          tradeoffs: result.exp1.synthesisMetrics.tradeoffs - deliberationMetrics.tradeoffs,
          keyPoints: result.exp1.synthesisMetrics.keyPoints - deliberationMetrics.keyPoints,
          unresolvedQuestions: result.exp1.synthesisMetrics.unresolvedQuestions - deliberationMetrics.unresolvedQuestions,
          recommendedActions: result.exp1.synthesisMetrics.recommendedActions - deliberationMetrics.recommendedActions,
          wordCount: result.exp1.synthesisMetrics.wordCount - deliberationMetrics.wordCount,
        };
      }
      if (result.exp2?.perModelResults) {
        result.exp2.deltas = {};
        for (const [modelKey, mr] of Object.entries(result.exp2.perModelResults)) {
          if (mr.synthesisMetrics) {
            result.exp2.deltas[modelKey] = {
              tradeoffs: mr.synthesisMetrics.tradeoffs - deliberationMetrics.tradeoffs,
              keyPoints: mr.synthesisMetrics.keyPoints - deliberationMetrics.keyPoints,
              unresolvedQuestions: mr.synthesisMetrics.unresolvedQuestions - deliberationMetrics.unresolvedQuestions,
              recommendedActions: mr.synthesisMetrics.recommendedActions - deliberationMetrics.recommendedActions,
              wordCount: mr.synthesisMetrics.wordCount - deliberationMetrics.wordCount,
            };
          }
        }
      }
    }

    questionResults[q.id] = result;

    // Save incrementally after each question
    const output = {
      experiment: 'controlled-baselines',
      description: 'Prompt-matched controlled baselines for Paper 03: (1) aggregation-only, (2) self-refinement per model. All prompts match run-discussion.js deliberation prompts.',
      hyperparameters: HYPERPARAMS,
      runMetadata: {
        startedAt: new Date(startTime).toISOString(),
        lastUpdated: new Date().toISOString(),
        totalApiCalls,
        questionsCompleted: Object.keys(questionResults).length,
        questionsTotal: QUESTIONS.length,
      },
      questionResults,
    };

    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    fs.writeFileSync(outputPath, JSON.stringify(output, null, 2));
    console.log(`  Saved (${Object.keys(questionResults).length}/${QUESTIONS.length} questions)`);

    // Wait between questions
    if (qi < questions.length - 1) {
      await sleep(HYPERPARAMS.delayBetweenQuestionsMs);
    }
  }

  // Final summary
  const elapsed = ((Date.now() - startTime) / 1000 / 60).toFixed(1);
  console.log(`\n${'='.repeat(70)}`);
  console.log(`COMPLETE: ${Object.keys(questionResults).length} questions, ${totalApiCalls} API calls, ${elapsed} min`);
  console.log(`Results: ${outputPath}`);
  console.log('='.repeat(70));

  // Print comparison table
  printSummaryTable(questionResults);
}

function printSummaryTable(questionResults) {
  console.log(`\n${'='.repeat(90)}`);
  console.log('COMPARISON: Aggregation-Only vs Self-Refinement vs Deliberation');
  console.log('='.repeat(90));
  console.log(`${'Question'.padEnd(35)} ${'Delib'.padEnd(12)} ${'Agg-Only'.padEnd(12)} ${'SR-Claude'.padEnd(12)} ${'SR-Gemini'.padEnd(12)} ${'SR-GPT'.padEnd(12)}`);
  console.log('-'.repeat(90));

  for (const q of QUESTIONS) {
    const r = questionResults[q.id];
    if (!r) continue;

    const dMetrics = r.deliberationMetrics;
    const aMetrics = r.exp1?.synthesisMetrics;
    const srC = r.exp2?.perModelResults?.['claude-opus-4-6']?.synthesisMetrics;
    const srG = r.exp2?.perModelResults?.['gemini-3-pro']?.synthesisMetrics;
    const srP = r.exp2?.perModelResults?.['gpt-5-2']?.synthesisMetrics;

    const fmt = (m) => m ? `${m.tradeoffs}T/${m.unresolvedQuestions}U` : '---';

    console.log(`${q.title.slice(0, 33).padEnd(35)} ${fmt(dMetrics).padEnd(12)} ${fmt(aMetrics).padEnd(12)} ${fmt(srC).padEnd(12)} ${fmt(srG).padEnd(12)} ${fmt(srP).padEnd(12)}`);
  }

  console.log('\nLegend: T=Trade-offs, U=Unresolved questions');
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
