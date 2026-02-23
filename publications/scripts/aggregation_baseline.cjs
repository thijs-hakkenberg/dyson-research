#!/usr/bin/env node
/**
 * Aggregation-Only Baseline Experiment
 *
 * For each of the 16 deliberation questions:
 * 1. Read the three Round 1 proposals (stripping YAML frontmatter)
 * 2. Send them to Claude Opus 4.6 with a synthesis prompt (no voting/scores/deliberation context)
 * 3. Count in both aggregation-only synthesis and full deliberation conclusion:
 *    (a) explicit trade-offs identified
 *    (b) distinct divergent topics
 * 4. Compare and save results
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// ── Configuration ──────────────────────────────────────────────────────────────
const DATABRICKS_TOKEN = process.env.DATABRICKS_TOKEN;
const DATABRICKS_WORKSPACE = process.env.DATABRICKS_WORKSPACE || 'https://dbc-51a89e1e-48db.cloud.databricks.com';
const API_ENDPOINT = `${DATABRICKS_WORKSPACE}/serving-endpoints/databricks-claude-opus-4-6/invocations`;
const MAX_TOKENS = 8000;
const TEMPERATURE = 0.3;
const DELAY_MS = 30000; // 30 seconds between API calls

const BASE_DIR = path.join(__dirname, '..', '..', 'src', 'content', 'research-questions');
const OUTPUT_PATH = path.join(__dirname, '..', 'drafts', '03-multi-model-ai-consensus', 'aggregation-baseline-results.json');

// ── Question list ──────────────────────────────────────────────────────────────
const QUESTIONS = [
  'phase-0/rq-0-14-propellant-production-phase-0-scope',
  'phase-0/rq-0-18-human-rating-transport-vehicles',
  'phase-0/rq-0-26-dual-bucket-wheel-excavation',
  'phase-0/rq-0-28-isru-cost-methodology-validation',
  'phase-0/rq-0-29-multi-century-governance-structure',
  'phase-1/rq-1-11-swarm-power-architecture-end-use',
  'phase-1/rq-1-16-autonomous-assembly-certification',
  'phase-1/rq-1-21-feedstock-acquisition-isru-timeline',
  'phase-1/rq-1-24-swarm-coordination-architecture-scale',
  'phase-1/rq-1-33-tug-end-of-life-disposal',
  'phase-1/rq-1-40-slot-reallocation-governance',
  'phase-1/rq-1-42-node-end-of-life-disposal',
  'phase-2/rq-2-17-fleet-coordination-scale-constraints',
  'phase-2/rq-2-20-swarm-roi-threshold-humanity-power-needs',
  'phase-2/rq-2-3-billion-unit-collision-avoidance',
  'phase-2/rq-2-8-autonomous-repair-authority-limits',
];

// ── Helpers ────────────────────────────────────────────────────────────────────

/**
 * Strip YAML frontmatter from markdown content
 */
function stripFrontmatter(content) {
  const match = content.match(/^---\n[\s\S]*?\n---\n/);
  if (match) {
    return content.slice(match[0].length).trim();
  }
  return content.trim();
}

/**
 * Read a markdown file and strip its frontmatter
 */
function readProposal(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  return stripFrontmatter(content);
}

/**
 * Sleep for ms milliseconds
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Call the Databricks Claude API
 */
function callClaudeAPI(prompt) {
  return new Promise((resolve, reject) => {
    const url = new URL(API_ENDPOINT);
    const isHttps = url.protocol === 'https:';
    const lib = isHttps ? https : http;

    const body = JSON.stringify({
      messages: [
        { role: 'user', content: prompt }
      ],
      max_tokens: MAX_TOKENS,
      temperature: TEMPERATURE,
    });

    const options = {
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

    const req = lib.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            const parsed = JSON.parse(data);
            const text = parsed.choices?.[0]?.message?.content || '';
            resolve(text);
          } catch (e) {
            reject(new Error(`JSON parse error: ${e.message}\nRaw: ${data.slice(0, 500)}`));
          }
        } else {
          reject(new Error(`API error ${res.statusCode}: ${data.slice(0, 500)}`));
        }
      });
    });

    req.on('error', reject);
    req.setTimeout(120000, () => {
      req.destroy();
      reject(new Error('Request timeout (120s)'));
    });
    req.write(body);
    req.end();
  });
}

/**
 * Build the synthesis prompt (no voting, scores, winners, or deliberation context)
 */
function buildSynthesisPrompt(proposal1, proposal2, proposal3) {
  return `You are a technical synthesis editor. Below are three independent engineering proposals addressing the same question. Please synthesize these into a single conclusion document with the following sections:
1. Summary (2-3 paragraphs synthesizing the key conclusions)
2. Key Points (4-6 areas where the proposals agree)
3. Trade-offs (list each engineering trade-off where proposals disagree, with the competing positions)
4. Unresolved Questions (2-4 areas requiring further analysis)
5. Recommended Actions (3-5 concrete next steps)

Here are the three proposals:

[PROPOSAL 1 - Claude]
${proposal1}

[PROPOSAL 2 - Gemini]
${proposal2}

[PROPOSAL 3 - GPT]
${proposal3}`;
}

/**
 * Count explicit trade-offs in text.
 * Looks for:
 * - Lines in a "Trade-offs" section
 * - Explicit "trade-off" mentions with context
 * - "versus" / "vs." patterns indicating competing positions
 * - Numbered/bulleted items in trade-off sections
 */
function countTradeoffs(text) {
  const lines = text.split('\n');
  let inTradeoffSection = false;
  let tradeoffCount = 0;
  const tradeoffPatterns = new Set();

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();

    // Detect trade-off section headers
    if (/^#+\s*trade[- ]?off/i.test(line) ||
        /^#+\s*divergent/i.test(line) ||
        /^#+\s*areas?\s+of\s+disagree/i.test(line) ||
        /^#+\s*competing\s+positions/i.test(line)) {
      inTradeoffSection = true;
      continue;
    }

    // Detect end of trade-off section (next major heading)
    if (inTradeoffSection && /^#+\s+/.test(line) &&
        !/trade[- ]?off/i.test(line) &&
        !/divergent/i.test(line)) {
      inTradeoffSection = false;
    }

    // Count items in trade-off sections
    if (inTradeoffSection) {
      // Numbered items: "1.", "2.", etc. or bold items: "**something**"
      if (/^\d+[\.\)]\s+/.test(line) || /^[-*]\s+\*\*/.test(line) || /^[-*]\s+\S/.test(line)) {
        // Avoid counting sub-items that are just elaboration
        if (line.length > 15) {
          tradeoffCount++;
        }
      }
    }
  }

  // Also count explicit "trade-off" phrases outside sections as a fallback
  if (tradeoffCount === 0) {
    const tradeoffMentions = text.match(/trade[- ]?off/gi) || [];
    // Each unique trade-off mention in context
    for (const match of tradeoffMentions) {
      tradeoffCount++;
    }
    // Deduplicate roughly
    tradeoffCount = Math.ceil(tradeoffCount / 2); // mentions usually come in pairs (intro + detail)
  }

  return Math.max(tradeoffCount, 0);
}

/**
 * Count distinct divergent topics in text.
 * Looks for:
 * - Items in "Unresolved Questions" / "Divergent Views" / "Open Questions" sections
 * - Explicit disagreement markers
 */
function countDivergentTopics(text) {
  const lines = text.split('\n');
  let inDivergentSection = false;
  let divergentCount = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();

    // Detect divergent/unresolved section headers
    if (/^#+\s*unresolved/i.test(line) ||
        /^#+\s*divergent/i.test(line) ||
        /^#+\s*open\s+question/i.test(line) ||
        /^#+\s*areas?\s+of\s+disagree/i.test(line) ||
        /^#+\s*remaining\s+disagree/i.test(line) ||
        /^#+\s*unresolved\s+question/i.test(line)) {
      inDivergentSection = true;
      continue;
    }

    // Detect end of section
    if (inDivergentSection && /^#+\s+/.test(line) &&
        !/unresolved/i.test(line) &&
        !/divergent/i.test(line) &&
        !/open\s+question/i.test(line)) {
      inDivergentSection = false;
    }

    // Count items in divergent sections
    if (inDivergentSection) {
      if (/^\d+[\.\)]\s+/.test(line) || /^[-*]\s+\*\*/.test(line)) {
        if (line.length > 15) {
          divergentCount++;
        }
      }
    }
  }

  return Math.max(divergentCount, 0);
}

/**
 * Extract the question's human-readable name from the slug
 */
function questionName(slug) {
  const parts = slug.split('/');
  const name = parts[parts.length - 1]
    .replace(/^rq-\d+-\d+-/, '')
    .replace(/-/g, ' ');
  return name.charAt(0).toUpperCase() + name.slice(1);
}

// ── Main ───────────────────────────────────────────────────────────────────────
async function main() {
  if (!DATABRICKS_TOKEN) {
    console.error('ERROR: DATABRICKS_TOKEN environment variable is not set.');
    console.error('Run: export $(cat .env | xargs)');
    process.exit(1);
  }

  console.log(`Aggregation-Only Baseline Experiment`);
  console.log(`====================================`);
  console.log(`API endpoint: ${API_ENDPOINT}`);
  console.log(`Temperature: ${TEMPERATURE}`);
  console.log(`Max tokens: ${MAX_TOKENS}`);
  console.log(`Delay between calls: ${DELAY_MS}ms`);
  console.log(`Questions: ${QUESTIONS.length}`);
  console.log();

  const results = [];
  let completed = 0;
  let failed = 0;

  for (let i = 0; i < QUESTIONS.length; i++) {
    const q = QUESTIONS[i];
    const qDir = path.join(BASE_DIR, q);
    const name = questionName(q);

    console.log(`[${i + 1}/${QUESTIONS.length}] ${name}`);

    try {
      // Read Round 1 proposals
      const claudeProposal = readProposal(path.join(qDir, 'round-1', 'claude-opus-4-6.md'));
      const geminiProposal = readProposal(path.join(qDir, 'round-1', 'gemini-3-pro.md'));
      const gptProposal = readProposal(path.join(qDir, 'round-1', 'gpt-5-2.md'));

      // Read full deliberation conclusion
      const conclusion = readProposal(path.join(qDir, 'conclusion.md'));

      // Build and send synthesis prompt
      const prompt = buildSynthesisPrompt(claudeProposal, geminiProposal, gptProposal);

      console.log(`  Calling API for aggregation-only synthesis...`);
      const synthesis = await callClaudeAPI(prompt);
      console.log(`  Received synthesis (${synthesis.length} chars)`);

      // Count metrics
      const aggTradeoffs = countTradeoffs(synthesis);
      const aggDivergent = countDivergentTopics(synthesis);
      const delibTradeoffs = countTradeoffs(conclusion);
      const delibDivergent = countDivergentTopics(conclusion);

      const result = {
        question: q,
        name: name,
        aggregation: {
          tradeoffs: aggTradeoffs,
          divergentTopics: aggDivergent,
          synthesisLength: synthesis.length,
        },
        deliberation: {
          tradeoffs: delibTradeoffs,
          divergentTopics: delibDivergent,
          conclusionLength: conclusion.length,
        },
        delta: {
          tradeoffs: delibTradeoffs - aggTradeoffs,
          divergentTopics: delibDivergent - aggDivergent,
        },
        aggregationSynthesis: synthesis,
      };

      results.push(result);
      completed++;

      console.log(`  Aggregation: ${aggTradeoffs} trade-offs, ${aggDivergent} divergent topics`);
      console.log(`  Deliberation: ${delibTradeoffs} trade-offs, ${delibDivergent} divergent topics`);
      console.log(`  Delta: ${result.delta.tradeoffs > 0 ? '+' : ''}${result.delta.tradeoffs} trade-offs, ${result.delta.divergentTopics > 0 ? '+' : ''}${result.delta.divergentTopics} divergent topics`);

      // Wait before next API call (except for last one)
      if (i < QUESTIONS.length - 1) {
        console.log(`  Waiting ${DELAY_MS / 1000}s before next call...`);
        await sleep(DELAY_MS);
      }

    } catch (err) {
      console.error(`  FAILED: ${err.message}`);
      failed++;

      results.push({
        question: q,
        name: name,
        error: err.message,
      });

      // Still wait even on failure
      if (i < QUESTIONS.length - 1) {
        console.log(`  Waiting ${DELAY_MS / 1000}s before next call...`);
        await sleep(DELAY_MS);
      }
    }
  }

  // ── Compute summary statistics ─────────────────────────────────────────────
  const successful = results.filter(r => !r.error);
  const summary = {
    totalQuestions: QUESTIONS.length,
    completed: completed,
    failed: failed,
    timestamp: new Date().toISOString(),
    model: 'claude-opus-4-6',
    temperature: TEMPERATURE,
    maxTokens: MAX_TOKENS,
  };

  if (successful.length > 0) {
    const aggTradeoffs = successful.map(r => r.aggregation.tradeoffs);
    const delibTradeoffs = successful.map(r => r.deliberation.tradeoffs);
    const aggDivergent = successful.map(r => r.aggregation.divergentTopics);
    const delibDivergent = successful.map(r => r.deliberation.divergentTopics);

    const mean = arr => arr.reduce((a, b) => a + b, 0) / arr.length;
    const sum = arr => arr.reduce((a, b) => a + b, 0);

    summary.aggregationMeans = {
      tradeoffs: mean(aggTradeoffs).toFixed(2),
      divergentTopics: mean(aggDivergent).toFixed(2),
    };
    summary.deliberationMeans = {
      tradeoffs: mean(delibTradeoffs).toFixed(2),
      divergentTopics: mean(delibDivergent).toFixed(2),
    };
    summary.aggregationTotals = {
      tradeoffs: sum(aggTradeoffs),
      divergentTopics: sum(aggDivergent),
    };
    summary.deliberationTotals = {
      tradeoffs: sum(delibTradeoffs),
      divergentTopics: sum(delibDivergent),
    };

    // Count how many questions had more trade-offs in deliberation vs aggregation
    summary.deliberationBetter = {
      tradeoffs: successful.filter(r => r.delta.tradeoffs > 0).length,
      divergentTopics: successful.filter(r => r.delta.divergentTopics > 0).length,
    };
    summary.aggregationBetter = {
      tradeoffs: successful.filter(r => r.delta.tradeoffs < 0).length,
      divergentTopics: successful.filter(r => r.delta.divergentTopics < 0).length,
    };
    summary.tied = {
      tradeoffs: successful.filter(r => r.delta.tradeoffs === 0).length,
      divergentTopics: successful.filter(r => r.delta.divergentTopics === 0).length,
    };
  }

  // ── Save results ───────────────────────────────────────────────────────────
  const output = {
    experiment: 'aggregation-only-baseline',
    description: 'Compare aggregation-only synthesis (Round 1 proposals only, no deliberation context) against full deliberation conclusions',
    summary,
    results: results.map(r => {
      // Save without the full synthesis text to keep the JSON manageable
      const { aggregationSynthesis, ...rest } = r;
      return rest;
    }),
    // Store syntheses separately for reference
    syntheses: results.filter(r => !r.error).map(r => ({
      question: r.question,
      synthesis: r.aggregationSynthesis,
    })),
  };

  fs.mkdirSync(path.dirname(OUTPUT_PATH), { recursive: true });
  fs.writeFileSync(OUTPUT_PATH, JSON.stringify(output, null, 2));
  console.log(`\nResults saved to: ${OUTPUT_PATH}`);

  // ── Print summary ──────────────────────────────────────────────────────────
  console.log(`\n${'='.repeat(60)}`);
  console.log(`SUMMARY`);
  console.log(`${'='.repeat(60)}`);
  console.log(`Completed: ${completed}/${QUESTIONS.length}`);
  console.log(`Failed: ${failed}/${QUESTIONS.length}`);

  if (successful.length > 0) {
    console.log(`\nMean trade-offs identified:`);
    console.log(`  Aggregation-only: ${summary.aggregationMeans.tradeoffs}`);
    console.log(`  Full deliberation: ${summary.deliberationMeans.tradeoffs}`);
    console.log(`\nMean divergent topics:`);
    console.log(`  Aggregation-only: ${summary.aggregationMeans.divergentTopics}`);
    console.log(`  Full deliberation: ${summary.deliberationMeans.divergentTopics}`);
    console.log(`\nTotal trade-offs:`);
    console.log(`  Aggregation-only: ${summary.aggregationTotals.tradeoffs}`);
    console.log(`  Full deliberation: ${summary.deliberationTotals.tradeoffs}`);
    console.log(`\nTotal divergent topics:`);
    console.log(`  Aggregation-only: ${summary.aggregationTotals.divergentTopics}`);
    console.log(`  Full deliberation: ${summary.deliberationTotals.divergentTopics}`);
    console.log(`\nDeliberation had more trade-offs: ${summary.deliberationBetter.tradeoffs}/${successful.length} questions`);
    console.log(`Aggregation had more trade-offs: ${summary.aggregationBetter.tradeoffs}/${successful.length} questions`);
    console.log(`Tied on trade-offs: ${summary.tied.tradeoffs}/${successful.length} questions`);
    console.log(`\nDeliberation had more divergent topics: ${summary.deliberationBetter.divergentTopics}/${successful.length} questions`);
    console.log(`Aggregation had more divergent topics: ${summary.aggregationBetter.divergentTopics}/${successful.length} questions`);
    console.log(`Tied on divergent topics: ${summary.tied.divergentTopics}/${successful.length} questions`);
  }

  // Per-question table
  if (successful.length > 0) {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`PER-QUESTION RESULTS`);
    console.log(`${'='.repeat(60)}`);
    console.log(`${'Question'.padEnd(45)} Agg(T/D)  Delib(T/D)  Delta(T/D)`);
    console.log(`${'-'.repeat(45)} --------  ----------  ----------`);
    for (const r of successful) {
      const shortName = r.name.slice(0, 43).padEnd(45);
      const agg = `${String(r.aggregation.tradeoffs).padStart(2)}/${String(r.aggregation.divergentTopics).padEnd(2)}`;
      const delib = `${String(r.deliberation.tradeoffs).padStart(2)}/${String(r.deliberation.divergentTopics).padEnd(2)}`;
      const dt = r.delta.tradeoffs >= 0 ? `+${r.delta.tradeoffs}` : `${r.delta.tradeoffs}`;
      const dd = r.delta.divergentTopics >= 0 ? `+${r.delta.divergentTopics}` : `${r.delta.divergentTopics}`;
      console.log(`${shortName} ${agg.padEnd(9)} ${delib.padEnd(11)} ${dt}/${dd}`);
    }
  }
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
