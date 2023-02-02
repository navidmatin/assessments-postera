from app.internals.route_helper import RouteHelper
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

import rdkit.Chem as Chem
import rdkit.Chem.Draw

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://localhost:5100"
]
# If using VSCode + windows, try using your IP
# instead (see frontent terminal)
# origins = [
#    "http://X.X.X.X:3000",
#    "X.X.X.X:3000"
# ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


async def make_d3_routes():
    routes = await RouteHelper.load_routes()
    view_routes = []
    for route in routes:
        view_routes.append(
            {'score': route.score, 'molecule': RouteHelper.create_d3_tree_from_route(
                route)})
    return view_routes


def draw_molecule(smiles: str, height: int, width: int):
    mol = Chem.MolFromSmiles(smiles)
    img = Chem.Draw.MolsToGridImage(
        [mol], molsPerRow=1, subImgSize=[height, width], useSVG=True)
    return img


@ app.get("/", tags=["root"])
async def read_root() -> dict:
    return {
        "message": "Welcome to your app.",
    }


@ app.get("/molecule", tags=["molecule"])
async def get_molecule(smiles: str, height: int = 200, width: int = 200) -> dict:
    molecule = draw_molecule(smiles, height, width)
    return Response(content=molecule, media_type="image/svg+xml")


@ app.get("/routes", tags=["routes"])
async def get_routes() -> dict:
    routes = await make_d3_routes()
    return {
        "data": routes,
    }
