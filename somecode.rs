// rustimport:pyo3
// Set the library's version and add a dependency:
//: [package]
//: version = "0.0.1"
//:
//: [dependencies]
//: rand = "0.8.5"
use pyo3::prelude::*;
use rand::prelude::{IteratorRandom, SliceRandom};

#[pyfunction]  // ← expose the function to Python
fn rebuild_and_generate(x: String, amount: usize) -> String {
	let markov_model = build_markov_model(&x);
    let generated_text = generate_text(&markov_model, amount);
	generated_text
}


fn custom_punctuation(c: char) -> bool {
    c == '.' || c == '!' || c == '?'
}

fn build_markov_model(text: &str) -> std::collections::HashMap<&str, Vec<&str>> {
    let words: Vec<&str> = text.split_whitespace().collect();
    let mut model = std::collections::HashMap::new();

    for i in 0..words.len() - 1 {
        let current_word = words[i];
        let next_word = words[i + 1];

        model
            .entry(current_word)
            .or_insert_with(Vec::new)
            .push(next_word);
    }

    model
}

fn generate_text(model: &std::collections::HashMap<&str, Vec<&str>>, num_sentences: usize) -> String {
    let mut rng = rand::thread_rng();
    let mut generated_text = Vec::new();
    let mut current_word = if let Some(start_word_candidates) = model.keys().cloned().filter(|&word| word.chars().next().unwrap().is_uppercase()).collect::<Vec<_>>().choose(&mut rng) {
        start_word_candidates
    } else {
        model.keys().cloned().choose(&mut rng).unwrap()
    };

	let mut sentence_count = 0;
    while sentence_count < num_sentences {
        if let Some(next_word_options) = model.get(&current_word) {
            if let Some(&next_word) = next_word_options.choose(&mut rand::thread_rng()) {
                generated_text.push(next_word);
                current_word = next_word;

                // Check for the presence of a punctuation mark
                if custom_punctuation(next_word.chars().last().unwrap_or_default()) {
                    // Increase sentence count only if it's a punctuation mark
                    sentence_count += 1;
                }
            }
        } else {
            // Randomize the next word if it's not found in the model. Maybe should make it choose from the actual first words of different sentences.
            let random_word = model.keys().choose(&mut rand::thread_rng()).unwrap();
            generated_text.push(*random_word);
            current_word = *random_word;
        }
    }

    generated_text.join(" ")
}
