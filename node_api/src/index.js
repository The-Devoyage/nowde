import express from "express";
import cors from "cors";
import helmet from "helmet";
import controllers from "./controllers/index.js";

const app = express();
const port = 3000;

app.use(helmet());
app.use(cors());

app.use("/", controllers);

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
