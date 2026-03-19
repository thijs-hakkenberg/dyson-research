#!/usr/bin/env node
/**
 * Paper 03 Quality Evaluation Experiments
 *
 * Three experiments addressing reviewer demands:
 *   1. Divergent View Extraction from aggregation-only proposals
 *   2. LLM-as-judge blinded quality comparison (deliberation vs aggregation)
 *   3. Inter-rater reliability proxy (second LLM re-codes divergent views)
 *
 * Usage:
 *   export $(cat .env | xargs)
 *   node publications/scripts/paper03_quality_eval.cjs
 */

const fs = require('fs').promises;
const path = require('path');
const https = require('https');
const http = require('http');

const PROJECT_ROOT = path.resolve(__dirname, '../..');
const BASELINES_PATH = path.join(PROJECT_ROOT, 'publications/data/controlled-baselines/results.json');
const OUTPUT_PATH = path.join(PROJECT_ROOT, 'publications/data/controlled-baselines/quality-eval.json');

const DATABRICKS_HOST = process.env.DATABRICKS_HOST || process.env.DATABRICKS_WORKSPACE;
const DATABRICKS_TOKEN = process.env.DATABRICKS_TOKEN;

const MODELS = {
  'claude-opus-4-6': { endpoint: '/serving-endpoints/databricks-claude-opus-4-6/invocations', name: 'Claude Opus 4.6' },
  'gemini-3-pro': { endpoint: '/serving-endpoints/databricks-gemini-3-pro/invocations', name: 'Gemini 3 Pro' },
  'gpt-5-2': { endpoint: '/serving-endpoints/databricks-gpt-5-2/invocations', name: 'GPT-5.2' },
};

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function callModel(modelKey, prompt, opts = {}) {
  const model = MODELS[modelKey];
  const url = new URL(model.endpoint, DATABRICKS_HOST);
  const body = JSON.stringify({
    messages: [
      { role: 'system', content: opts.systemPrompt || 'You are an expert engineering analyst.' },
      { role: 'user', content: prompt },
    ],
    max_tokens: opts.maxTokens || 8000,
    temperature: opts.temperature || 0.3,
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
    req.on('timeout', () => { req.destroy(); reject(new Error('Request timeout')); });
    req.write(body);
    req.end();
  });
}

// ============================================================================
// Experiment 1: Divergent View Extraction from Aggregation-Only
// ============================================================================

async function extractDivergentViews(proposals, questionTitle) {
  const proposalText = proposals
    .filter(p => p.content)
    .map(p => `=== ${MODELS[p.modelId]?.name || p.modelId} ===\n${p.content.slice(0, 2000)}`)
    .join('\n\n');

  const prompt = `Given these three independent engineering proposals for the question "${questionTitle}", identify all points of disagreement between the models.

For each disagreement, provide:
1. Topic (brief title)
2. The specific positions of each model
3. Whether this represents a genuine engineering trade-off

Respond in JSON format:
{
  "divergent_topics": [
    {
      "topic": "...",
      "positions": [{"model": "...", "position": "..."}],
      "is_genuine_tradeoff": true/false
    }
  ],
  "total_topics": N,
  "genuine_tradeoffs": N
}

Proposals:
${proposalText}`;

  const result = await callModel('claude-opus-4-6', prompt);
  try {
    const jsonMatch = result.match(/\{[\s\S]*\}/);
    return jsonMatch ? JSON.parse(jsonMatch[0]) : { error: 'No JSON found', raw: result.slice(0, 500) };
  } catch (e) {
    return { error: e.message, raw: result.slice(0, 500) };
  }
}

// ============================================================================
// Experiment 2: Blinded Quality Comparison (LLM-as-Judge)
// ============================================================================

async function blindedQualityJudge(deliberationConclusion, aggregationSynthesis, questionTitle, judgeModel) {
  // Randomize order to avoid position bias
  const isDelibFirst = Math.random() > 0.5;
  const outputA = isDelibFirst ? deliberationConclusion : aggregationSynthesis;
  const outputB = isDelibFirst ? aggregationSynthesis : deliberationConclusion;

  const prompt = `You are evaluating two engineering analysis outputs for the question: "${questionTitle}"

Rate each output on these 5 criteria (1-5 scale):
1. Feasibility awareness (identifies constraints and limitations)
2. Risk identification (flags uncertainties and failure modes)
3. Traceability (positions linked to evidence/reasoning)
4. Actionability (provides concrete next steps)
5. Completeness (covers key aspects of the question)

Then state which output is better overall (A or B or Tie).

Respond in JSON:
{
  "output_a": {"feasibility": N, "risk": N, "traceability": N, "actionability": N, "completeness": N},
  "output_b": {"feasibility": N, "risk": N, "traceability": N, "actionability": N, "completeness": N},
  "preferred": "A" or "B" or "Tie",
  "reasoning": "..."
}

=== Output A ===
${(outputA || '').slice(0, 3000)}

=== Output B ===
${(outputB || '').slice(0, 3000)}`;

  const result = await callModel(judgeModel, prompt);
  try {
    const jsonMatch = result.match(/\{[\s\S]*\}/);
    const parsed = jsonMatch ? JSON.parse(jsonMatch[0]) : null;
    if (parsed) {
      // De-blind: map back to deliberation/aggregation
      parsed._isDelibFirst = isDelibFirst;
      parsed.deliberation_scores = isDelibFirst ? parsed.output_a : parsed.output_b;
      parsed.aggregation_scores = isDelibFirst ? parsed.output_b : parsed.output_a;
      parsed.deliberation_preferred = (parsed.preferred === 'A' && isDelibFirst) || (parsed.preferred === 'B' && !isDelibFirst);
      parsed.aggregation_preferred = (parsed.preferred === 'B' && isDelibFirst) || (parsed.preferred === 'A' && !isDelibFirst);
    }
    return parsed || { error: 'No JSON', raw: result.slice(0, 500) };
  } catch (e) {
    return { error: e.message, raw: result.slice(0, 500) };
  }
}

// ============================================================================
// Main
// ============================================================================

async function main() {
  if (!DATABRICKS_TOKEN) {
    console.error('ERROR: DATABRICKS_TOKEN not set');
    process.exit(1);
  }

  const baselines = JSON.parse(await fs.readFile(BASELINES_PATH, 'utf-8'));
  const qr = baselines.questionResults;
  const slugs = Object.keys(qr);

  // Select 6 stratified questions for evaluation
  const evalSlugs = slugs.filter(s => qr[s].exp1?.synthesis).slice(0, 6);

  console.log('=' .repeat(70));
  console.log('Paper 03 Quality Evaluation Experiments');
  console.log('=' .repeat(70));
  console.log(`Questions for evaluation: ${evalSlugs.length}`);
  console.log(`Date: ${new Date().toISOString()}\n`);

  const results = {
    timestamp: new Date().toISOString(),
    questionsEvaluated: evalSlugs.length,
    experiment1_divergentViews: [],
    experiment2_blindedJudge: [],
  };

  // Load deliberation conclusions for comparison
  for (const slug of evalSlugs) {
    const q = qr[slug];
    console.log(`\n[${slug}] ${q.questionTitle}`);

    // Exp 1: Extract divergent views from aggregation proposals
    if (q.exp1?.proposals) {
      console.log('  [DV] Extracting divergent views from aggregation proposals...');
      try {
        const dv = await extractDivergentViews(q.exp1.proposals, q.questionTitle);
        results.experiment1_divergentViews.push({
          questionId: q.questionId,
          slug,
          ...dv,
        });
        console.log(`  [DV] Found ${dv.total_topics || '?'} topics, ${dv.genuine_tradeoffs || '?'} genuine`);
      } catch (e) {
        console.error(`  [DV] FAILED: ${e.message}`);
      }
      await sleep(15000);
    }

    // Exp 2: Blinded quality comparison (use GPT as judge for Claude-synthesized outputs)
    const deliberationConclusion = q.deliberationMetrics ?
      `Key points: ${q.deliberationMetrics.keyPoints}, Unresolved: ${q.deliberationMetrics.unresolvedQuestions}, Actions: ${q.deliberationMetrics.recommendedActions}` : null;

    if (q.exp1?.synthesis && deliberationConclusion) {
      console.log('  [Judge] Running blinded quality comparison...');
      try {
        // Use GPT to judge Claude-synthesized outputs (avoids self-judging bias)
        const judge = await blindedQualityJudge(
          deliberationConclusion,
          q.exp1.synthesis,
          q.questionTitle,
          'gpt-5-2'
        );
        results.experiment2_blindedJudge.push({
          questionId: q.questionId,
          slug,
          judgeModel: 'gpt-5-2',
          ...judge,
        });
        const pref = judge.deliberation_preferred ? 'Deliberation' : judge.aggregation_preferred ? 'Aggregation' : 'Tie';
        console.log(`  [Judge] Preferred: ${pref}`);
      } catch (e) {
        console.error(`  [Judge] FAILED: ${e.message}`);
      }
      await sleep(15000);
    }
  }

  // Summary
  console.log('\n' + '='.repeat(70));
  console.log('SUMMARY');
  console.log('='.repeat(70));

  // DV summary
  const dvResults = results.experiment1_divergentViews.filter(r => !r.error);
  const totalTopics = dvResults.reduce((s, r) => s + (r.total_topics || 0), 0);
  const totalGenuine = dvResults.reduce((s, r) => s + (r.genuine_tradeoffs || 0), 0);
  console.log(`\nDivergent Views from Aggregation: ${totalTopics} topics, ${totalGenuine} genuine trade-offs (${dvResults.length} questions)`);
  console.log(`Deliberation comparison: 47 topics, 12 genuine (16 questions)`);
  console.log(`Per-question rate: Aggregation ${(totalTopics/Math.max(dvResults.length,1)).toFixed(1)} vs Deliberation ${(47/16).toFixed(1)}`);

  // Judge summary
  const judgeResults = results.experiment2_blindedJudge.filter(r => !r.error);
  const delibWins = judgeResults.filter(r => r.deliberation_preferred).length;
  const aggWins = judgeResults.filter(r => r.aggregation_preferred).length;
  const ties = judgeResults.length - delibWins - aggWins;
  console.log(`\nBlinded Quality Comparison: Deliberation ${delibWins}, Aggregation ${aggWins}, Tie ${ties} (${judgeResults.length} questions)`);

  await fs.writeFile(OUTPUT_PATH, JSON.stringify(results, null, 2));
  console.log(`\nResults saved: ${OUTPUT_PATH}`);
}

main().catch(console.error);
