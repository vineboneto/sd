import { fork } from "child_process";
import { connect } from "http2";
import { io } from "socket.io-client";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1) + min);
}

if (process.argv[2] !== "client") {
  // Criação de 4 processos de cliente
  for (let i = 0; i < 4; i++) {
    const clientProcess = fork(__filename, ["client", i + 1]);
  }
} else {
  // Clientes 10 minutos adiantados
  let date = new Date();
  date.setMinutes(date.getMinutes() + getRandomInt(1, 100));
  const id = process.argv[3];
  console.log(`Processo criado ${id}, initial date: ${date.toISOString()}`);

  const socket = io("http://localhost:3000");

  socket.on("connect", () => {
    console.log(`Processo ${id} conectado ao servidor`);
  });

  socket.on("sync:time", (serverDate) => {
    const diffInMs = date.getTime() - new Date(serverDate).getTime();

    const response = { clientId: id, diff: diffInMs / 1000 };

    socket.emit("sync:diff", response);
  });

  socket.on("sync:time:client", (diffTime) => {
    date.setSeconds(date.getSeconds() + diffTime);

    console.log(`Process ${id} new date: ${date.toISOString()}`);
  });

  socket.on("disconnect", (socket) => {
    console.log(`Processo ${id} desconectado do servidor`);
  });
}
