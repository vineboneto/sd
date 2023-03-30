const net = require("net");

const socket = new net.Socket();

socket.connect(5000, "localhost", () => {
  console.log("Conectado ao servidor!");

  // Envia a primeira mensagem "ping"
  socket.write("ping");
});

socket.on("data", (data) => {
  const message = data.toString().trim();
  console.log(`Mensagem recebida do servidor: "${message}"`);

  // Verifica se a mensagem recebida é "pong" ou "ok", e envia a próxima mensagem correspondente
  if (message === "pong") {
    socket.write("alo");
  } else if (message === "ok") {
    // Envia uma mensagem vazia para manter a conexão aberta
    socket.write("");
  }
});

socket.on("end", () => {
  console.log("Conexão encerrada!");
});

function sendMessage(message) {
  // console.log(`Enviando mensagem "${message}" para o servidor...`);
  // const length = Buffer.byteLength(message, "utf8");
  // const header = Buffer.from([0x81, length]);
  // const payload = Buffer.from(message, "utf8");
  // socket.write(Buffer.concat([header, payload]));
}
