#!/usr/bin/env node
/**
 * Self-Refinement Baseline Experiment (Experiment 2)
 *
 * For a stratified subset of 4 questions (one per convergence category),
 * run a single model through a generate -> critique -> refine loop for the
 * same number of rounds as multi-model deliberation took for that question.
 * Compare output quality against the deliberation conclusion.
 *
 * Stratified selection:
 *   1. Rapid convergence (1 round): rq-0-26 Dual bucket-wheel excavation
 *   2. Moderate convergence (2 rounds): rq-1-24 Swarm coordination architecture
 *   3. Slow convergence (3 rounds): rq-0-28 ISRU cost methodology validation
 *   4. Governance/non-technical (1 round): rq-0-29 Multi-century governance
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// -- Configuration -----------------------------------------------------------
const DATABRICKS_TOKEN = process.env.DATABRICKS_TOKEN;
const DATABRICKS_WORKSPACE = process.env.DATABRICKS_WORKSPACE || 'https://dbc-51a89e1e-48db.cloud.databricks.com';
const API_ENDPOINT = `${DATABRICKS_WORKSPACE}/serving-endpoints/databricks-claude-opus-4-6/invocations`;
const MAX_TOKENS = 8000;
const TEMPERATURE = 0.7; // Same as deliberation
const DELAY_MS = 45000;  // 45 seconds between API calls

const BASE_DIR = path.join(__dirname, '..', '..', 'src', 'content', 'research-questions');
const OUTPUT_PATH = path.join(__dirname, '..', 'drafts', '03-multi-model-ai-consensus', 'self-refinement-results.json');

// -- Question selection (stratified) -----------------------------------------
const QUESTIONS = [
  {
    path: 'phase-0/rq-0-26-dual-bucket-wheel-excavation',
    slug: 'dual-bucket-wheel-excavation',
    title: 'Dual counter-rotating bucket-wheel excavation for microgravity torque balancing',
    category: 'rapid',
    deliberationRounds: 1,
  },
  {
    path: 'phase-1/rq-1-24-swarm-coordination-architecture-scale',
    slug: 'swarm-coordination-architecture-scale',
    title: 'Swarm coordination architecture at scale (millions of units)',
    category: 'moderate',
    deliberationRounds: 2,
  },
  {
    path: 'phase-0/rq-0-28-isru-cost-methodology-validation',
    slug: 'isru-cost-methodology-validation',
    title: 'In-situ resource utilization cost methodology validation',
    category: 'slow',
    deliberationRounds: 3,
  },
  {
    path: 'phase-0/rq-0-29-multi-century-governance-structure',
    slug: 'multi-century-governance-structure',
    title: 'Governance structure for multi-century, volunteer-driven global coordination',
    category: 'governance',
    deliberationRounds: 1,
  },
];

// -- Helpers -----------------------------------------------------------------

function stripFrontmatter(content) {
  const match = content.match(/^---\n[\s\S]*?\n---\n/);
  if (match) return content.slice(match[0].length).trim();
  return content.trim();
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function callClaudeAPI(systemPrompt, userPrompt) {
  return new Promise((resolve, reject) => {
    const url = new URL(API_ENDPOINT);
    const isHttps = url.protocol === 'https:';
    const lib = isHttps ? https : http;

    const messages = [];
    if (systemPrompt) {
      messages.push({ role: 'system', content: systemPrompt });
    }
    messages.push({ role: 'user', content: userPrompt });

    const body = JSON.stringify({
      messages,
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
    req.setTimeout(180000, () => {
      req.destroy();
      reject(new Error('Request timeout (180s)'));
    });
    req.write(body);
    req.end();
  });
}

// -- Prompt templates --------------------------------------------------------

function round1Prompt(questionText) {
  return `You are an expert in space systems engineering, orbital mechanics, and mission design. Please provide a comprehensive proposal (up to 2000 words) addressing the following engineering question:

${questionText}

Structure your proposal with: Summary, Technical Analysis, Trade-offs, Risk Assessment, and Recommended Approach.`;
}

function selfRefinementPrompt(questionText, previousProposal) {
  return `You previously proposed the following in response to an engineering question. Please critically review your own proposal, identify weaknesses, gaps, or alternative approaches you may have overlooked, and provide an improved version (up to 2000 words).

Original question: ${questionText}

Your previous proposal:
${previousProposal}

Please provide: (1) a self-critique identifying 3-5 weaknesses, (2) an improved proposal addressing those weaknesses.`;
}

function synthesisConclusionPrompt(questionText, finalProposal) {
  return `Based on your refined analysis, please provide a final conclusion document for the following question:

${questionText}

Your final refined proposal:
${finalProposal}

Structure the conclusion with:
1. Summary (2-3 paragraphs)
2. Key Points (4-6 agreed conclusions)
3. Trade-offs (list engineering trade-offs with competing positions)
4. Unresolved Questions (2-4 areas requiring further analysis)
5. Recommended Actions (3-5 concrete next steps)`;
}

// -- Metrics extraction ------------------------------------------------------

/**
 * Detect if a line is a section header matching a keyword pattern.
 * Handles formats like: ## Trade-offs, ## 3. Trade-offs, ## 3 Trade-offs
 */
function isSectionHeader(line, patterns) {
  if (!/^#+\s+/.test(line)) return false;
  const headerText = line.replace(/^#+\s+/, '').replace(/^\d+[\.\):]?\s*/, '');
  return patterns.some(p => p.test(headerText));
}

/**
 * Count top-level items in a section. Handles:
 * - Numbered items: "1. Text", "1) Text"
 * - Bold list items: "- **Text**"
 * - Sub-headings as items: "### 3.1. Title"
 * - Bold paragraph items (only if no sub-headings found): "**2.1. Text**"
 *
 * Two-pass approach: first count sub-headings; if none found, count inline items.
 */
function countSectionItems(text, sectionPatterns) {
  const lines = text.split('\n');
  let inSection = false;
  let sectionLevel = 0;
  let subHeadingCount = 0;
  let inlineCount = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;

    // Check for section entry
    if (!inSection && isSectionHeader(line, sectionPatterns)) {
      inSection = true;
      sectionLevel = (line.match(/^#+/) || [''])[0].length;
      continue;
    }

    // Check for section exit (same or higher level heading that doesn't match)
    if (inSection && /^#+\s+/.test(line)) {
      const level = (line.match(/^#+/) || [''])[0].length;
      if (level <= sectionLevel) {
        const headerText = line.replace(/^#+\s+/, '').replace(/^\d+[\.\):]?\s*/, '');
        const stillInSection = sectionPatterns.some(p => p.test(headerText));
        if (!stillInSection) {
          inSection = false;
          continue;
        }
      }
      // Sub-heading within section counts as an item
      if (level > sectionLevel && line.length > 15) {
        subHeadingCount++;
        continue;
      }
    }

    if (inSection) {
      // Numbered items at top level: "1. Text" or "1) Text"
      if (/^\d+[\.\)]\s+/.test(line) && line.length > 15) {
        inlineCount++;
      }
      // Bold list items: "- **Text**"
      else if (/^[-*]\s+\*\*/.test(line) && line.length > 15) {
        inlineCount++;
      }
      // Bold paragraph items: "**2.1. Text**", "**2.1 — Text**"
      // But NOT field labels
      else if (/^\*\*[\d\.\s—–\-]*[A-Z]/.test(line) && line.length > 15 &&
               !/^\*\*(Objective|Rationale|Deliverable|Note|Effect|Observation|Example|Evidence|Status|Context|Source|Impact|Mitigation|Pro|Con|Resolution|Risk|Position|Counter|Recommendation|Implication|Mechanism|Challenge|Problem|Tension|Question|Key|Why|What|How|When|Where|Who)s?[\s:]?:/i.test(line)) {
        inlineCount++;
      }
    }
  }

  // Prefer sub-heading count if available; otherwise use inline count
  if (subHeadingCount > 0) return subHeadingCount;
  return Math.max(inlineCount, 0);
}

function countTradeoffs(text) {
  const count = countSectionItems(text, [
    /^trade[- ]?off/i,
    /^divergent/i,
    /^areas?\s+of\s+disagree/i,
    /^competing\s+positions/i,
  ]);

  if (count > 0) return count;

  // Fallback: count trade-off mentions
  const mentions = text.match(/trade[- ]?off/gi) || [];
  return Math.max(Math.ceil(mentions.length / 2), 0);
}

function countUnresolvedQuestions(text) {
  return countSectionItems(text, [
    /^unresolved/i,
    /^open\s+question/i,
    /^remaining/i,
  ]);
}

function countRecommendedActions(text) {
  return countSectionItems(text, [
    /^recommended\s+action/i,
    /^next\s+step/i,
    /^action\s+item/i,
  ]);
}

function countKeyPoints(text) {
  return countSectionItems(text, [
    /^key\s+point/i,
    /^key\s+findings/i,
    /^key\s+points?\s+of\s+agree/i,
    /^points?\s+of\s+agree/i,
  ]);
}

function wordCount(text) {
  return text.trim().split(/\s+/).filter(w => w.length > 0).length;
}

function extractMetrics(text) {
  return {
    tradeoffs: countTradeoffs(text),
    keyPoints: countKeyPoints(text),
    unresolvedQuestions: countUnresolvedQuestions(text),
    recommendedActions: countRecommendedActions(text),
    wordCount: wordCount(text),
    charCount: text.length,
  };
}

// -- Recount from saved results -----------------------------------------------

function recountFromSaved() {
  console.log('RECOUNT MODE: Reloading saved results and recounting metrics.');
  const saved = JSON.parse(fs.readFileSync(OUTPUT_PATH, 'utf-8'));
  const results = saved.results;

  for (const r of results) {
    if (r.error) {
      console.log(`  SKIPPED (error): ${r.questionSlug}`);
      continue;
    }

    // Recount self-refinement conclusion metrics
    const srText = r.selfRefinementConclusion;
    r.selfRefinementMetrics = extractMetrics(srText);

    // Recount deliberation conclusion metrics
    const qDir = path.join(BASE_DIR,
      QUESTIONS.find(q => q.slug === r.questionSlug).path);
    const delibText = stripFrontmatter(
      fs.readFileSync(path.join(qDir, 'conclusion.md'), 'utf-8'));
    r.deliberationMetrics = extractMetrics(delibText);

    // Recompute delta
    r.delta = {
      tradeoffs: r.selfRefinementMetrics.tradeoffs - r.deliberationMetrics.tradeoffs,
      keyPoints: r.selfRefinementMetrics.keyPoints - r.deliberationMetrics.keyPoints,
      unresolvedQuestions: r.selfRefinementMetrics.unresolvedQuestions - r.deliberationMetrics.unresolvedQuestions,
      recommendedActions: r.selfRefinementMetrics.recommendedActions - r.deliberationMetrics.recommendedActions,
      wordCount: r.selfRefinementMetrics.wordCount - r.deliberationMetrics.wordCount,
    };

    console.log(`  ${r.questionSlug}: SR(${r.selfRefinementMetrics.tradeoffs}/${r.selfRefinementMetrics.unresolvedQuestions}/${r.selfRefinementMetrics.recommendedActions}/${r.selfRefinementMetrics.wordCount}) Delib(${r.deliberationMetrics.tradeoffs}/${r.deliberationMetrics.unresolvedQuestions}/${r.deliberationMetrics.recommendedActions}/${r.deliberationMetrics.wordCount})`);
  }

  saved.summary = computeSummary(results);
  saved.config.recountedAt = new Date().toISOString();
  fs.writeFileSync(OUTPUT_PATH, JSON.stringify(saved, null, 2));
  console.log(`\nRecounted results saved to: ${OUTPUT_PATH}`);
  printComparisonTable(results);
}

// -- Main --------------------------------------------------------------------

const RECOUNT_MODE = process.argv.includes('--recount');
const RETRY_FAILED = process.argv.includes('--retry-failed');

async function main() {
  // In recount mode, reload saved results and recount metrics
  if (RECOUNT_MODE) {
    return recountFromSaved();
  }

  if (!DATABRICKS_TOKEN) {
    console.error('ERROR: DATABRICKS_TOKEN environment variable is not set.');
    console.error('Run: export $(cat /Users/hakketh/projects/experiments/dyson/.env | xargs)');
    process.exit(1);
  }

  console.log('Self-Refinement Baseline Experiment (Experiment 2)');
  console.log('==================================================');
  console.log(`API endpoint: ${API_ENDPOINT}`);
  console.log(`Temperature: ${TEMPERATURE}`);
  console.log(`Max tokens: ${MAX_TOKENS}`);
  console.log(`Delay between calls: ${DELAY_MS / 1000}s`);
  console.log(`Questions: ${QUESTIONS.length}`);
  console.log(`Retry failed: ${RETRY_FAILED}`);
  console.log();

  // Load existing results if retrying
  let existingResults = [];
  if (RETRY_FAILED && fs.existsSync(OUTPUT_PATH)) {
    const saved = JSON.parse(fs.readFileSync(OUTPUT_PATH, 'utf-8'));
    existingResults = saved.results || [];
    console.log(`Loaded ${existingResults.length} existing results.`);
  }

  const results = [];

  for (let qi = 0; qi < QUESTIONS.length; qi++) {
    const q = QUESTIONS[qi];
    const qDir = path.join(BASE_DIR, q.path);
    const totalRounds = q.deliberationRounds;

    console.log(`\n${'='.repeat(60)}`);
    console.log(`[${qi + 1}/${QUESTIONS.length}] ${q.title}`);
    console.log(`  Category: ${q.category} | Deliberation rounds: ${totalRounds}`);
    console.log(`${'='.repeat(60)}`);

    // Skip if already completed in retry mode
    if (RETRY_FAILED) {
      const existing = existingResults.find(r => r.questionSlug === q.slug && !r.error);
      if (existing) {
        console.log('  SKIPPED (already completed)');
        results.push(existing);
        continue;
      }
    }

    try {
      // Read the question text (markdown body)
      const questionFilePath = path.join(BASE_DIR, q.path + '.md')
        .replace(/\/rq-(\d+-\d+)-/, '/rq-$1-');
      // The .md file is at the phase level, not inside the discussion dir
      // e.g. phase-0/rq-0-26-dual-bucket-wheel-excavation.md
      const questionMdPath = path.join(BASE_DIR,
        q.path.split('/')[0],
        q.path.split('/')[1] + '.md');
      const questionFullText = stripFrontmatter(fs.readFileSync(questionMdPath, 'utf-8'));

      // Read full deliberation conclusion for comparison
      const conclusionText = stripFrontmatter(
        fs.readFileSync(path.join(qDir, 'conclusion.md'), 'utf-8'));

      // Self-refinement loop
      const rounds = [];
      let currentProposal = '';

      for (let round = 1; round <= totalRounds; round++) {
        console.log(`\n  --- Round ${round}/${totalRounds} ---`);

        let response;
        if (round === 1) {
          // Initial generation
          console.log('  Generating initial proposal...');
          const prompt = round1Prompt(questionFullText);
          response = await callClaudeAPI(null, prompt);
          console.log(`  Received (${response.length} chars, ${wordCount(response)} words)`);
        } else {
          // Self-refinement
          console.log('  Generating self-critique and refined proposal...');
          const prompt = selfRefinementPrompt(questionFullText, currentProposal);
          response = await callClaudeAPI(null, prompt);
          console.log(`  Received (${response.length} chars, ${wordCount(response)} words)`);
        }

        currentProposal = response;
        rounds.push({
          round,
          type: round === 1 ? 'initial' : 'self-refinement',
          content: response,
          wordCount: wordCount(response),
          charCount: response.length,
        });

        // Wait between API calls
        if (round < totalRounds || true) { // always wait before synthesis
          console.log(`  Waiting ${DELAY_MS / 1000}s...`);
          await sleep(DELAY_MS);
        }
      }

      // Final synthesis into conclusion format
      console.log('\n  --- Final Synthesis ---');
      console.log('  Generating conclusion document...');
      const conclusionPrompt = synthesisConclusionPrompt(questionFullText, currentProposal);
      const selfRefinementConclusion = await callClaudeAPI(null, conclusionPrompt);
      console.log(`  Received conclusion (${selfRefinementConclusion.length} chars, ${wordCount(selfRefinementConclusion)} words)`);

      // Extract metrics from both conclusions
      const srMetrics = extractMetrics(selfRefinementConclusion);
      const delibMetrics = extractMetrics(conclusionText);

      console.log(`\n  Metrics comparison:`);
      console.log(`  ${'Metric'.padEnd(25)} Self-Refine  Deliberation`);
      console.log(`  ${'-'.repeat(25)} -----------  ------------`);
      console.log(`  ${'Trade-offs'.padEnd(25)} ${String(srMetrics.tradeoffs).padStart(11)}  ${String(delibMetrics.tradeoffs).padStart(12)}`);
      console.log(`  ${'Key points'.padEnd(25)} ${String(srMetrics.keyPoints).padStart(11)}  ${String(delibMetrics.keyPoints).padStart(12)}`);
      console.log(`  ${'Unresolved questions'.padEnd(25)} ${String(srMetrics.unresolvedQuestions).padStart(11)}  ${String(delibMetrics.unresolvedQuestions).padStart(12)}`);
      console.log(`  ${'Recommended actions'.padEnd(25)} ${String(srMetrics.recommendedActions).padStart(11)}  ${String(delibMetrics.recommendedActions).padStart(12)}`);
      console.log(`  ${'Word count'.padEnd(25)} ${String(srMetrics.wordCount).padStart(11)}  ${String(delibMetrics.wordCount).padStart(12)}`);

      results.push({
        questionSlug: q.slug,
        questionTitle: q.title,
        category: q.category,
        deliberationRounds: q.deliberationRounds,
        selfRefinementRounds: totalRounds,
        totalAPICalls: totalRounds + 1, // rounds + synthesis
        selfRefinementMetrics: srMetrics,
        deliberationMetrics: delibMetrics,
        delta: {
          tradeoffs: srMetrics.tradeoffs - delibMetrics.tradeoffs,
          keyPoints: srMetrics.keyPoints - delibMetrics.keyPoints,
          unresolvedQuestions: srMetrics.unresolvedQuestions - delibMetrics.unresolvedQuestions,
          recommendedActions: srMetrics.recommendedActions - delibMetrics.recommendedActions,
          wordCount: srMetrics.wordCount - delibMetrics.wordCount,
        },
        selfRefinementConclusion: selfRefinementConclusion,
        rounds: rounds.map(r => ({
          round: r.round,
          type: r.type,
          wordCount: r.wordCount,
          charCount: r.charCount,
          content: r.content,
        })),
      });

      // Wait before next question
      if (qi < QUESTIONS.length - 1) {
        console.log(`\n  Waiting ${DELAY_MS / 1000}s before next question...`);
        await sleep(DELAY_MS);
      }

    } catch (err) {
      console.error(`  FAILED: ${err.message}`);
      results.push({
        questionSlug: q.slug,
        questionTitle: q.title,
        category: q.category,
        deliberationRounds: q.deliberationRounds,
        error: err.message,
      });

      if (qi < QUESTIONS.length - 1) {
        console.log(`  Waiting ${DELAY_MS / 1000}s before next question...`);
        await sleep(DELAY_MS);
      }
    }
  }

  // -- Save results -----------------------------------------------------------
  const successful = results.filter(r => !r.error);
  const output = {
    experiment: 'self-refinement-baseline',
    description: 'Single-model self-refinement baseline (Experiment 2): generate -> critique -> refine loop matching deliberation round count, compared against multi-model deliberation conclusions.',
    config: {
      model: 'claude-opus-4-6',
      temperature: TEMPERATURE,
      maxTokens: MAX_TOKENS,
      delayMs: DELAY_MS,
      timestamp: new Date().toISOString(),
    },
    summary: computeSummary(results),
    results,
  };

  fs.mkdirSync(path.dirname(OUTPUT_PATH), { recursive: true });
  fs.writeFileSync(OUTPUT_PATH, JSON.stringify(output, null, 2));
  console.log(`\nResults saved to: ${OUTPUT_PATH}`);

  // -- Print comparison table ------------------------------------------------
  printComparisonTable(results);
}

function computeSummary(results) {
  const successful = results.filter(r => !r.error);
  if (successful.length === 0) return { completed: 0, failed: results.length };

  const mean = arr => arr.length === 0 ? 0 : arr.reduce((a, b) => a + b, 0) / arr.length;

  return {
    completed: successful.length,
    failed: results.filter(r => r.error).length,
    selfRefinement: {
      meanTradeoffs: +mean(successful.map(r => r.selfRefinementMetrics.tradeoffs)).toFixed(2),
      meanKeyPoints: +mean(successful.map(r => r.selfRefinementMetrics.keyPoints)).toFixed(2),
      meanUnresolved: +mean(successful.map(r => r.selfRefinementMetrics.unresolvedQuestions)).toFixed(2),
      meanActions: +mean(successful.map(r => r.selfRefinementMetrics.recommendedActions)).toFixed(2),
      meanWordCount: +mean(successful.map(r => r.selfRefinementMetrics.wordCount)).toFixed(0),
    },
    deliberation: {
      meanTradeoffs: +mean(successful.map(r => r.deliberationMetrics.tradeoffs)).toFixed(2),
      meanKeyPoints: +mean(successful.map(r => r.deliberationMetrics.keyPoints)).toFixed(2),
      meanUnresolved: +mean(successful.map(r => r.deliberationMetrics.unresolvedQuestions)).toFixed(2),
      meanActions: +mean(successful.map(r => r.deliberationMetrics.recommendedActions)).toFixed(2),
      meanWordCount: +mean(successful.map(r => r.deliberationMetrics.wordCount)).toFixed(0),
    },
  };
}

function printComparisonTable(results) {
  const successful = results.filter(r => !r.error);
  if (successful.length === 0) {
    console.log('\nNo successful results to display.');
    return;
  }

  console.log(`\n${'='.repeat(80)}`);
  console.log('SELF-REFINEMENT vs DELIBERATION: COMPARISON TABLE');
  console.log(`${'='.repeat(80)}`);

  // Header
  console.log(`\n${'Question'.padEnd(30)} Cat.     Rds  ` +
    `SR(T/U/A/W)       Delib(T/U/A/W)`);
  console.log(`${'-'.repeat(30)} ------   ---  ` +
    `${''.padEnd(18, '-')} ${''.padEnd(18, '-')}`);

  for (const r of successful) {
    const shortTitle = r.questionTitle.slice(0, 28).padEnd(30);
    const cat = r.category.slice(0, 6).padEnd(8);
    const rds = String(r.deliberationRounds).padEnd(4);
    const sr = `${r.selfRefinementMetrics.tradeoffs}/${r.selfRefinementMetrics.unresolvedQuestions}/${r.selfRefinementMetrics.recommendedActions}/${r.selfRefinementMetrics.wordCount}`;
    const dl = `${r.deliberationMetrics.tradeoffs}/${r.deliberationMetrics.unresolvedQuestions}/${r.deliberationMetrics.recommendedActions}/${r.deliberationMetrics.wordCount}`;
    console.log(`${shortTitle} ${cat} ${rds} ${sr.padEnd(18)} ${dl}`);
  }

  console.log(`\nLegend: T=Trade-offs, U=Unresolved questions, A=Recommended actions, W=Word count`);

  // Summary
  const s = computeSummary(results);
  console.log(`\n${'='.repeat(80)}`);
  console.log('SUMMARY MEANS');
  console.log(`${'='.repeat(80)}`);
  console.log(`${'Metric'.padEnd(25)} Self-Refinement  Deliberation  Delta`);
  console.log(`${'-'.repeat(25)} ---------------  ------------  -----`);
  console.log(`${'Trade-offs'.padEnd(25)} ${String(s.selfRefinement.meanTradeoffs).padStart(15)}  ${String(s.deliberation.meanTradeoffs).padStart(12)}  ${(s.selfRefinement.meanTradeoffs - s.deliberation.meanTradeoffs >= 0 ? '+' : '') + (s.selfRefinement.meanTradeoffs - s.deliberation.meanTradeoffs).toFixed(2)}`);
  console.log(`${'Unresolved questions'.padEnd(25)} ${String(s.selfRefinement.meanUnresolved).padStart(15)}  ${String(s.deliberation.meanUnresolved).padStart(12)}  ${(s.selfRefinement.meanUnresolved - s.deliberation.meanUnresolved >= 0 ? '+' : '') + (s.selfRefinement.meanUnresolved - s.deliberation.meanUnresolved).toFixed(2)}`);
  console.log(`${'Recommended actions'.padEnd(25)} ${String(s.selfRefinement.meanActions).padStart(15)}  ${String(s.deliberation.meanActions).padStart(12)}  ${(s.selfRefinement.meanActions - s.deliberation.meanActions >= 0 ? '+' : '') + (s.selfRefinement.meanActions - s.deliberation.meanActions).toFixed(2)}`);
  console.log(`${'Word count'.padEnd(25)} ${String(s.selfRefinement.meanWordCount).padStart(15)}  ${String(s.deliberation.meanWordCount).padStart(12)}  ${(s.selfRefinement.meanWordCount - s.deliberation.meanWordCount >= 0 ? '+' : '') + (s.selfRefinement.meanWordCount - s.deliberation.meanWordCount).toFixed(0)}`);
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
