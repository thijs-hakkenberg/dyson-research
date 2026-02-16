#!/usr/bin/env node

/**
 * Multi-Model Peer Review Script
 *
 * Sends paper drafts to Claude, Gemini, and GPT for structured academic peer review,
 * then synthesizes a comparative summary.
 *
 * Usage:
 *   # Review both versions A and B
 *   source .env
 *   node publications/scripts/peer-review-paper.js --paper=01-isru-economic-crossover
 *
 *   # Review single version
 *   node publications/scripts/peer-review-paper.js --paper=01-isru-economic-crossover --version=a
 *
 *   # Summary only (from existing reviews)
 *   node publications/scripts/peer-review-paper.js --paper=01-isru-economic-crossover --summary-only
 *
 * Environment variables:
 *   DATABRICKS_TOKEN - API token for Databricks
 *   DATABRICKS_HOST  - Databricks host URL (optional, has default)
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '../..');
const DRAFTS_DIR = path.join(PROJECT_ROOT, 'publications/drafts');

// Configuration
const DATABRICKS_HOST = process.env.DATABRICKS_HOST || process.env.DATABRICKS_WORKSPACE || 'https://adb-6239133969168510.10.azuredatabricks.net';
const DATABRICKS_TOKEN = process.env.DATABRICKS_TOKEN;

const MODELS = {
  'claude-opus-4-6': {
    id: 'databricks-claude-opus-4-6',
    name: 'Claude Opus 4.6',
    filename: 'claude-opus-4-6.md',
    endpoint: '/serving-endpoints/databricks-claude-opus-4-6/invocations'
  },
  'gemini-3-pro': {
    id: 'databricks-gemini-3-pro',
    name: 'Gemini 3 Pro',
    filename: 'gemini-3-pro.md',
    endpoint: '/serving-endpoints/databricks-gemini-3-pro/invocations',
    maxTokens: 65000
  },
  'gpt-5-2': {
    id: 'databricks-gpt-5-2',
    name: 'GPT-5.2',
    filename: 'gpt-5-2.md',
    endpoint: '/serving-endpoints/databricks-gpt-5-2/invocations'
  }
};

const REVIEW_MODELS = ['claude-opus-4-6', 'gemini-3-pro', 'gpt-5-2'];

const SYSTEM_PROMPT = `You are an expert academic peer reviewer for a high-impact journal in space systems engineering, economics, and resource utilization. You have deep expertise in:

- Space resource economics (ISRU, lunar/asteroid mining)
- Parametric cost modeling and learning curve analysis
- Monte Carlo simulation methods
- Publication standards for journals like Acta Astronautica, Space Policy, and New Space

Provide a thorough, constructive peer review. Be specific with line references where possible. Your review should be rigorous but fair — acknowledge strengths as well as weaknesses.`;

function buildReviewPrompt(paperContent, version) {
  return `Please review the following academic paper manuscript (Version ${version.toUpperCase()}). The paper is provided in LaTeX source format.

## Paper Manuscript

\`\`\`latex
${paperContent}
\`\`\`

---

## Review Instructions

Provide a structured peer review with the following sections. For each criterion, assign a rating on a 1-5 scale:
- 5 = Excellent
- 4 = Good
- 3 = Adequate
- 2 = Needs Improvement
- 1 = Serious Concerns

### Review Criteria

For each criterion below, provide:
1. A numeric rating (1-5)
2. A narrative assessment (2-4 paragraphs)

**1. Significance & Novelty**
Is this an important and original contribution to the field? Does it address a meaningful gap in the literature? Would it advance understanding or practice?

**2. Methodological Soundness**
Are the methods robust, appropriate for the research questions, and reproducible? Are assumptions clearly stated and justified? Is the statistical/analytical approach valid?

**3. Validity & Logic**
Are conclusions supported by the data and analysis? Is the interpretation accurate and balanced? Are limitations acknowledged?

**4. Clarity & Structure**
Is the paper well-written and logically organized? Are figures and tables effective? Is the abstract accurate? Would a non-specialist reader follow the argument?

**5. Ethical Compliance**
Are there appropriate disclosures about AI-assisted methodology? Are conflicts of interest addressed? Is the research ethically sound?

**6. Scope & Referencing**
Is the paper appropriate for a space systems/economics journal? Are references sufficient, relevant, and up-to-date? Is prior work adequately acknowledged?

### Additional Sections

**Major Issues**
List any critical flaws that would require substantial revision or re-analysis. Be specific about what needs to change and why.

**Minor Issues**
List typographical errors, formatting issues, unclear passages, or small improvements. Reference specific sections or equations where possible.

**Overall Recommendation**
State one of: Accept / Minor Revision / Major Revision / Reject
Provide a 1-paragraph justification.

**Constructive Suggestions**
Provide 3-5 specific, actionable suggestions that would most improve the paper. Focus on high-impact changes.

---

Format your response as clean markdown with the section headers exactly as shown above.`;
}

/**
 * Query Databricks LLM API
 */
async function queryDatabricks(modelKey, systemPrompt, userPrompt) {
  if (!DATABRICKS_TOKEN) {
    console.error('DATABRICKS_TOKEN not set. Run: source .env');
    process.exit(1);
  }

  const model = MODELS[modelKey];
  const endpoint = `${DATABRICKS_HOST}${model.endpoint}`;

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${DATABRICKS_TOKEN}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: userPrompt }
        ],
        max_tokens: model.maxTokens || 100000,
        temperature: 0.7
      })
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`API error: ${response.status} - ${error}`);
    }

    const data = await response.json();
    const content = data.choices?.[0]?.message?.content;

    // Handle Gemini's array format where content is [{type: 'text', text: '...'}]
    if (Array.isArray(content)) {
      const textContent = content.find(c => c.type === 'text');
      return textContent?.text || null;
    }

    return content || data.content;
  } catch (error) {
    console.error(`Error querying ${model.name}:`, error.message);
    return null;
  }
}

/**
 * Load paper source from disk
 */
async function loadPaper(paperSlug, version) {
  const filename = `${paperSlug}-${version}.tex`;
  const filepath = path.join(DRAFTS_DIR, filename);

  try {
    return await fs.readFile(filepath, 'utf-8');
  } catch (error) {
    console.error(`Could not read paper: ${filepath}`);
    console.error(`  ${error.message}`);
    return null;
  }
}

/**
 * Save a review to disk
 */
async function saveReview(paperSlug, version, modelKey, content, recommendation) {
  const model = MODELS[modelKey];
  const outputDir = path.join(DRAFTS_DIR, 'reviews', `version-${version}`);
  const outputPath = path.join(outputDir, model.filename);

  await fs.mkdir(outputDir, { recursive: true });

  const date = new Date().toISOString().split('T')[0];
  const frontmatter = `---
paper: "${paperSlug}"
version: "${version}"
modelId: "${modelKey}"
modelName: "${model.name}"
reviewed: "${date}"
recommendation: "${recommendation}"
---

`;

  await fs.writeFile(outputPath, frontmatter + content, 'utf-8');
  console.log(`    Saved: ${outputPath}`);
}

/**
 * Extract recommendation from review content
 */
function extractRecommendation(content) {
  // Look for the Overall Recommendation section
  const match = content.match(/Overall Recommendation[*]*\s*\n+(?:State one of:.*\n+)?(?:\*\*)?(?:Recommendation:\s*)?(Accept|Minor Revision|Major Revision|Reject)/i);
  if (match) return match[1];

  // Fallback: look for any of the recommendation terms near the end
  const lower = content.toLowerCase();
  const lastSection = lower.slice(-2000);
  if (lastSection.includes('accept') && !lastSection.includes('major revision') && !lastSection.includes('minor revision')) return 'Accept';
  if (lastSection.includes('minor revision')) return 'Minor Revision';
  if (lastSection.includes('major revision')) return 'Major Revision';
  if (lastSection.includes('reject')) return 'Reject';

  return 'Unknown';
}

/**
 * Load existing review from disk
 */
async function loadReview(paperSlug, version, modelKey) {
  const model = MODELS[modelKey];
  const reviewPath = path.join(DRAFTS_DIR, 'reviews', `version-${version}`, model.filename);

  try {
    const content = await fs.readFile(reviewPath, 'utf-8');
    return content;
  } catch {
    return null;
  }
}

/**
 * Review a single version with a single model
 */
async function reviewVersion(paperSlug, version, modelKey, paperContent) {
  const model = MODELS[modelKey];
  console.log(`  ${model.name} reviewing version ${version.toUpperCase()}...`);

  const userPrompt = buildReviewPrompt(paperContent, version);
  const content = await queryDatabricks(modelKey, SYSTEM_PROMPT, userPrompt);

  if (!content) {
    console.log(`    ${model.name} API unavailable — skipping`);
    return null;
  }

  const recommendation = extractRecommendation(content);
  console.log(`    Recommendation: ${recommendation}`);

  await saveReview(paperSlug, version, modelKey, content, recommendation);
  return { modelKey, modelName: model.name, version, content, recommendation };
}

/**
 * Generate comparative summary from all reviews
 */
async function generateSummary(paperSlug, reviews) {
  console.log('\nGenerating comparative summary...');

  const reviewsText = reviews.map(r => {
    return `## ${r.modelName} — Version ${r.version.toUpperCase()}\n\nRecommendation: ${r.recommendation}\n\n${r.content}`;
  }).join('\n\n---\n\n');

  const summaryPrompt = `You are synthesizing peer reviews of an academic paper from 3 AI models, each reviewing 2 versions (A = formal academic voice, B = humanized voice).

## All Reviews

${reviewsText}

---

Generate a comparative summary document with EXACTLY these sections:

## Version Comparison

Compare how each version (A vs B) was received across all reviewers. Which voice style was preferred? Were there trade-offs in perceived rigor vs readability?

## Consensus Strengths

List 4-6 strengths that ALL or MOST reviewers agreed on. Be specific.

## Consensus Weaknesses

List 4-6 weaknesses that ALL or MOST reviewers identified. Be specific about what needs fixing.

## Divergent Opinions

List areas where reviewers disagreed. Attribute each position to the specific model.

## Aggregated Ratings

Create a markdown table:

| Criterion | Claude A | Claude B | Gemini A | Gemini B | GPT A | GPT B |
|-----------|----------|----------|----------|----------|-------|-------|

Extract numeric ratings from each review for: Significance & Novelty, Methodological Soundness, Validity & Logic, Clarity & Structure, Ethical Compliance, Scope & Referencing.

## Priority Action Items

List the top 5-7 most impactful changes to make, ranked by importance. For each, note which reviewers flagged it and whether it applies to version A, B, or both.

## Overall Assessment

A brief paragraph summarizing the paper's readiness for submission and which version to proceed with.`;

  const content = await queryDatabricks('claude-opus-4-6', SYSTEM_PROMPT, summaryPrompt);

  if (!content) {
    console.log('  Failed to generate summary');
    return null;
  }

  const outputPath = path.join(DRAFTS_DIR, 'reviews', 'summary.md');
  const date = new Date().toISOString().split('T')[0];
  const frontmatter = `---
paper: "${paperSlug}"
generated: "${date}"
type: "review-summary"
reviewers:
  - claude-opus-4-6
  - gemini-3-pro
  - gpt-5-2
---

`;

  await fs.writeFile(outputPath, frontmatter + content, 'utf-8');
  console.log(`  Saved: ${outputPath}`);

  return content;
}

/**
 * Main execution
 */
async function main() {
  const args = process.argv.slice(2);
  const paperSlug = args.find(a => a.startsWith('--paper='))?.split('=')[1];
  const versionFilter = args.find(a => a.startsWith('--version='))?.split('=')[1];
  const summaryOnly = args.includes('--summary-only');

  if (!paperSlug) {
    console.error('Usage: node publications/scripts/peer-review-paper.js --paper=<slug> [--version=a|b] [--summary-only]');
    process.exit(1);
  }

  const versions = versionFilter ? [versionFilter] : ['a', 'b'];

  console.log('='.repeat(60));
  console.log('Multi-Model Peer Review');
  console.log('='.repeat(60));
  console.log();
  console.log(`Paper: ${paperSlug}`);
  console.log(`Versions: ${versions.map(v => v.toUpperCase()).join(', ')}`);
  console.log(`Models: ${REVIEW_MODELS.map(m => MODELS[m].name).join(', ')}`);
  if (summaryOnly) console.log('Mode: Summary only (from existing reviews)');
  console.log();

  const allReviews = [];

  if (!summaryOnly) {
    // Load paper content for each version
    const paperContents = {};
    for (const version of versions) {
      const content = await loadPaper(paperSlug, version);
      if (!content) {
        console.error(`Skipping version ${version.toUpperCase()} — file not found`);
        continue;
      }
      paperContents[version] = content;
      console.log(`Loaded version ${version.toUpperCase()} (${content.length} chars)`);
    }

    if (Object.keys(paperContents).length === 0) {
      console.error('No paper versions found. Exiting.');
      process.exit(1);
    }

    // Query all models for all versions
    for (const version of Object.keys(paperContents)) {
      console.log(`\nReviewing version ${version.toUpperCase()}:`);

      // Run all models in parallel for this version
      const reviewPromises = REVIEW_MODELS.map(modelKey =>
        reviewVersion(paperSlug, version, modelKey, paperContents[version])
      );

      const results = await Promise.all(reviewPromises);
      for (const result of results) {
        if (result) allReviews.push(result);
      }
    }
  } else {
    // Load existing reviews
    console.log('Loading existing reviews...');
    for (const version of versions) {
      for (const modelKey of REVIEW_MODELS) {
        const content = await loadReview(paperSlug, version, modelKey);
        if (content) {
          const recommendation = extractRecommendation(content);
          allReviews.push({
            modelKey,
            modelName: MODELS[modelKey].name,
            version,
            content: content.replace(/^---[\s\S]*?---\n*/, ''),
            recommendation
          });
          console.log(`  Loaded: ${MODELS[modelKey].name} — version ${version.toUpperCase()} (${recommendation})`);
        }
      }
    }
  }

  console.log(`\nCollected ${allReviews.length} reviews total.`);

  // Generate summary if we have enough reviews
  if (allReviews.length >= 2) {
    await generateSummary(paperSlug, allReviews);
  } else {
    console.log('Insufficient reviews for summary (need at least 2).');
  }

  console.log();
  console.log('='.repeat(60));
  console.log('Peer review complete!');
  console.log(`Reviews: publications/drafts/reviews/`);
  console.log('='.repeat(60));
}

main().catch(console.error);
