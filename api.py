import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Inputs(BaseModel):
    inp: int
    inp2: str


@app.get("/exemplo")
def example() -> str:
    return "Olá Mundo"


@app.post("/exemplo2")
def create_example(inputs: Inputs) -> str:
    return inputs.inp2


@app.put("/exemplo3")
def update_example(inputs: Inputs) -> str:
    return inputs.inp2


@app.delete("/exemplo3")
def delete_example(inputs: Inputs) -> str:
    return f"Item com valor '{inputs.inp2}' foi deletado."


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
