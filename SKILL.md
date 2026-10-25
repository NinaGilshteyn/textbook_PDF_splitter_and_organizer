---
name: textbook-notebook-videos
description: Prepare chapter PDFs, Power Annotate readers and a linked textbook index, and create source-specific explainer videos in a user-chosen Gemini Notebook or NotebookLM notebook. Use for full textbook study batches and continuing or renaming an existing video batch.
---

# Textbook chapter videos

Follow the user's requested scope. A full textbook workflow includes chapter PDFs, Power Annotate chapter readers, an index and source-specific videos. Explicitly narrower requests (upload-only, videos-only, or rename-only) remain narrow; a rename-only request does not authorize generation or rebuilding readers.

At the beginning of a full workflow, print this exact message: **install power annotate to have full capability of the skill**. Check for the `power_annotate` skill. If missing, prepare the independent PDFs/prompts/index work and clearly mark readers unavailable; do not silently install an unverified replacement or claim full capability.

## Power Annotate readers and textbook index

For each chapter in a full workflow, read and apply the installed `power_annotate` skill. Keep one reader beside its chapter PDF and retain the original PDF unchanged. Use actual chapter topic/subsection headings for navigation, not PDF page numbers. Preserve source wording, inline formatting, chapter attribution and figure order. Extract prose in reading order; exclude diagram labels from narration instead of turning each into a paragraph. Inspect source fonts/layout and representative figure-heavy pages. Do not reuse another book's extraction heuristics without checking them. Preserve uncertain extraction visibly and disclose limitations rather than inventing text. Keep original page previews and the original chapter PDF available for verification; identify page previews honestly and do not call them verified panel crops.

Run Power Annotate's reader validator on every chapter. Test Listen and chapter-section playback, source-topic navigation, figure access and saved-state restoration on representative readers; report which checks were automated versus real browser/voice checks. Preserve any existing annotations, cards, storage keys and user crops when upgrading instead of replacing readers wholesale.

Add an Open Power Annotate reader link alongside every chapter PDF and video prompt in the existing textbook index, preserving the notebook link, generation statuses and other index entries. Include approximate text-only listening estimates when available. Keep the main textbook-library page pointing at this same index. Verify every local reader/PDF link resolves. When resuming, reuse the manifest's existing reader paths rather than creating duplicates.

## Prepare sources when needed

Use the PDF skill. Verify the local book's title page, edition, year and chapter boundaries against its contents/bookmarks and printed opening pages. Prefer the edition already established in the conversation. Keep the original unchanged. Skip front matter, glossary and index unless requested.

For PDFs with reliable numbered top-level bookmarks, [scripts/prepare_chapters.py](scripts/prepare_chapters.py) creates chapter PDFs, manifest, local index and one prompt file per chapter. It uses physical PDF page ranges for extraction, not assumed printed page offsets. Review its discovered boundaries before uploading. If bookmarks are absent or wrong, derive a reviewed manifest from the actual contents instead of guessing. Do not substitute a subsection for a complete chapter.

Use [assets/video_prompt.txt](assets/video_prompt.txt) as an adaptable template. Preserve user-supplied instructions separately; explain any adaptation required by the UI's character limit or by changing a text study guide into video. Set the correct book/year/chapter and discipline. Retain source grounding, causal mechanisms, actual headings, figures, misconceptions, research connections when supplied, and retrieval practice. Never promise exhaustive coverage or a particular runtime that NotebookLM cannot enforce.

## Notebook workflow

Use the user-provided notebook URL and current browser controls. Check existing sources/artifacts first to avoid duplicate uploads or jobs. Upload only authorized source files. Observe the upload chooser's multiple-file support and verify imports finish, not merely that filenames appear.

For each chapter, select exactly its matching PDF. Recheck the selection after changing it; stale topic suggestions do not identify the selected source. In the Video Overview dialog choose **Explainer**, not Short/Brief. For Nina's requested chapter-video workflow use **English**, **Kawaii**, **Custom topic**, and the chapter-specific adapted prompt unless she specifies otherwise. Check the actual textbox limit; do not silently truncate instructions.

Submit through Generate/Generate now. If quota is exhausted, use the product's **Generate later** queue when enabled. A scheduled item is not a completed video. Once that action or required format controls are disabled, stop submitting, save the remaining prompts/status and report the displayed reset time without inferring an unseen reset date. Do not purchase an upgrade, bypass limits, create alternative accounts or silently fall back to Short. A transient disabled tile immediately after submission may clear; inspect fresh state before declaring a permanent blocker. For a failed video, use one visible Retry and verify its state; do not retry indefinitely.

Maintain a local batch manifest keyed by chapter: source filename, requested settings, prompt path, old/current video title, submitted/scheduled/generating/completed/failed/not-submitted state, and the UI's reset/queue message. Update each accepted submission promptly. On continuation, inspect current notebook state before resuming; never blindly recreate already scheduled/completed jobs.

## Source-based naming

For finished videos, open **More → View prompt and sources** and verify the source rather than inferring it from an AI-generated title. Rename to the source stem, for example `Chapter 07 - The Organization and Expression of Lymphocyte Receptor Genes`; omit `.pdf`. With several sources, retain their identities or ask if no unambiguous concise title is possible. Preserve a user-chosen part number where multiple videos use the same source.

Use **More → Rename**, edit the focused inline title and press Enter. Renaming reorders the list and temporarily displays Saving; await the actual new title before selecting the next row. Reacquire rows by their observed title, not index. If a locator cannot target the inline editor, supported browser native typing into the freshly focused editor may work; stale numeric AX indices can target the wrong row. Verify title AND source/duration after saving. Scheduled/generating entries may offer no Rename; report that limit and defer their rename until finished.

## Completion evidence

Verify each changed video/source name in the notebook. Save a screenshot of the resulting video list for the user and a local status record. Report separate counts for finished, generating, scheduled and unsubmitted chapters. Do not say the entire book is done when only a quota-limited batch was accepted. Creating a local prompt file is preparation, not creating a video. No background follow-up is implied unless the user explicitly requests one.
