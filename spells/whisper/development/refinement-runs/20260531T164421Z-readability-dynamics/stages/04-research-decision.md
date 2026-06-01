# Stage 04: Research Decision

Status: `pass`

Mode: `bounded-research`

## Decision

External research is appropriate because the operator explicitly asked how academia studies the problem.

## Academic Map

1. Discourse structure studies how parts of a text relate to each other. Rhetorical Structure Theory is especially relevant because it treats coherent text as spans with functions such as evidence, background, elaboration, concession, and preparation.

2. Cohesion and coherence research studies how textual features help readers connect ideas. Coh-Metrix is relevant because it goes beyond simple word-length and sentence-length readability formulas into cohesion, discourse, world knowledge, syntax, and language features.

3. Cognitive load and multimedia learning research studies why continuous material can overload readers and why segmentation/signaling helps. This maps cleanly to Whisper's need for beats, cues, and learner-paced units.

4. Genre analysis studies expected rhetorical moves in a transport. Swales' CARS model is relevant for research-style introductions because it distinguishes establishing territory, establishing a niche, and occupying the niche.

5. Typography and information design research studies line length, spacing, columns, and screen-reading performance. This supports the HTML side, but should not be mistaken for the whole problem.

## Research Sources

- Rhetorical Structure Theory site, Simon Fraser University: https://www.sfu.ca/rst/01intro/intro.html
- Graesser, McNamara, Louwerse, and Cai, "Coh-Metrix: Analysis of text on cohesion and language": https://asu.elsevierpure.com/en/publications/coh-metrix-analysis-of-text-on-cohesion-and-language/
- Mayer and Pilegard, "Principles for Managing Essential Processing in Multimedia Learning": https://www.cambridge.org/core/books/abs/cambridge-handbook-of-multimedia-learning/principles-for-managing-essential-processing-in-multimedia-learning-segmenting-pretraining-and-modality-principles/DD24C2F48B9B1277CE59F78276110258
- Ling and van Schaik, "Optimal Line Length in Reading: A Literature Review": https://journals.uc.edu/index.php/vl/article/view/5765
- Purdue OWL, "Organization and the CARS Model": https://owl.purdue.edu/owl/general_writing/the_writing_process/organization_CARS_Model.html

## Local Translation

Whisper should not import these as academic jargon for the reader. It should use them as internal schema families:

- `discourse_move`
- `cohesion_signal`
- `cognitive_load`
- `genre_move`
- `visual_treatment`
- `review_anchor`

