const net = require("net");
const fs = require("node:fs");
const readline = require("node:readline");
const { stdin: input, stdout: output } = require("node:process");

const rl = readline.createInterface({ input, output });

async function question(question) {
  const promise = new Promise((resolve, reject) => {
    rl.question(question, resolve);
  });

  return promise;
}

const socket = new net.Socket();

const encodeMessage = (channel, message) =>
  JSON.stringify({ channel, message });

const decodeMessage = (message) => JSON.parse(message);

let name;

socket.connect(5000, "localhost", () => {
  console.log("Conectado ao servidor!");

  socket.write(encodeMessage("ping", ""));
});

socket.on("data", async (data) => {
  const message = data.toString().trim();

  const { channel, message: content } = decodeMessage(message);

  if (channel === "auth") {
    if (!content) {
      async function handleAuth() {
        name = await question("Digite o seu nome: ");
        const pass = await question("Digite a sua senha: ");

        socket.write(encodeMessage("auth", { name, pass }));
      }
      await handleAuth();
    } else {
      console.log("Is Authenticated");
      socket.write(encodeMessage("question-next", { name }));
    }
  }

  if (channel === "question") {
    async function handleQuestion() {
      const answer = await question(content?.questao);

      socket.write(
        encodeMessage("answer-question", {
          question: content?.questaoId,
          answer,
          name,
        })
      );

      socket.write(encodeMessage("question-next", { name }));
    }
    await handleQuestion();
  }

  if (channel === "question-finish") {
    console.log(content);
  }
});

socket.on("end", () => {
  console.log("Conexão encerrada!");
});
