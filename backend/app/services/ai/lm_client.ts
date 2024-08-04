import { LMStudioClient } from "@lmstudio/sdk";

async function main() {
  // Create a client to connect to LM Studio, then load a model
  const client = new LMStudioClient();
  const model = await client.llm.load("mlabonne/AlphaMonarch-7B-GGUF/alphamonarch-7b.Q2_K.gguf");

   // Predict!
   const prediction = model.respond([
    { role: "system", content: "You are a helpful AI assistant." },
    { role: "user", content: "What is the meaning of life?" },
  ]);
  for await (const text of prediction) {
    process.stdout.write(text);
  }
}

main();