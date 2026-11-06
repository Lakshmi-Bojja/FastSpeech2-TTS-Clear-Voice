
"""
Inference Telugu - Test Sentences T1-T4
"""
TEST_SENTENCES = ["న్యూరోఫార్మకోలాజికల్ పరిశోధనలో నూతన ఔషధాల ప్రభావాన్ని విశ్లేషించారు.", "తాడుపై అతని పట్టు చాలా బలంగా ఉంది. / ఆమె పట్టు చీరను ధరించి వేడుకకు వచ్చింది.", "పులి అడవిలో నిశ్శబ్దంగా నడిచింది.", "ఈ సమావేశం 2026 నవంబర్ 12వ తేదీ ఉదయం 10:45 గంటలకు ప్రారంభమవుతుంది, సమయానికి సిద్ధంగా ఉండండి."]
def synthesize(text, config, ckpt, out):
    print(f"Synthesizing Telugu: {text}")
if __name__ == "__main__":
    synthesize(TEST_SENTENCES[0], "config.yaml", "checkpoints/model.ckpt", "../Results/Telugu/test_generated_audios/T1.wav")
