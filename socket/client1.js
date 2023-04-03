const net = require("net");
const fs = require("node:fs");

const socket = new net.Socket();

const encodeMessage = (channel, message) =>
  JSON.stringify({ channel, message });

const decodeMessage = (message) => JSON.parse(message);

socket.connect(5000, "localhost", () => {
  console.log("Conectado ao servidor!");

  socket.write(encodeMessage("ping", ""));
});

socket.on("data", (data) => {
  const message = data.toString().trim();

  console.log(message);

  const { channel, message: content } = decodeMessage(message);

  console.log(`Mensagem recebida do servidor: "${content}"`);

  if (channel === "pong") {
    const file = fs.readFileSync("arquivo.txt", "utf-8");
    const base64 = Buffer.from(file).toString("base64");
    const message = encodeMessage("arquivo-transfer", {
      base64,
      name: "arquivo.txt",
    });
    socket.write(message);
  } else if (channel === "ok") {
    console.log("Arquivo enviado com sucesso!");
  }
});

socket.on("end", () => {
  console.log("Conexão encerrada!");
});
