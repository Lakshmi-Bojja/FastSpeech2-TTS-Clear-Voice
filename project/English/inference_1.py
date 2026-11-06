
"""
Inference English - Test Sentences E1-E4
"""
TEST_SENTENCES = ["The antidisestablishmentarianism movement gained considerable momentum during the parliamentary proceedings.", "a) The orchestra's conduct during the ceremony was praised by the audience. b) The researchers will conduct an experiment to evaluate the proposed method.", "The rhythm of the orchestra changed unexpectedly.", "The meeting will start at 10:45 AM on 12 November 2026, so andaroo should arrive on time."]
def synthesize(text, config, ckpt, out):
    print(f"Synthesizing: {text} -> {out}")
    # Text -> phoneme -> model -> mel -> HiFi-GAN -> wav
    # Save variance plots
if __name__ == "__main__":
    synthesize(TEST_SENTENCES[0], "config.yaml", "checkpoints/model.ckpt", "../Results/English/test_generated_audios/E1.wav")
