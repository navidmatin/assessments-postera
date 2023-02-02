import React, { useEffect, useState, useMemo } from "react";
import { ReactSVG } from "react-svg";
import Tree from "react-d3-tree";
import {
  Autocomplete,
  Card,
  CardContent,
  TextField,
  Typography,
} from "@mui/material";
import { Molecule } from "./Molecule";

export const Routes = () => {
  const [routes, setRoutes] = useState([]);
  const [selectedRouteIndex, setSelectedRouteIndex] = useState(null);
  const [isLoading, setLoading] = useState(true);

  const NODE_HIGHT = 200;
  const NODE_WIDTH = 200;

  const fetchRoutes = async () => {
    const response = await fetch("http://localhost:8000/routes");
    // If using VSCode + windows, try using your IP
    // instead (see frontent terminal)
    //const response = await fetch("http://X.X.X.X:8000/routes");
    const newRoutes = await response.json();
    setRoutes(newRoutes.data);
    setLoading(false);
  };

  useEffect(() => {
    fetchRoutes();
  }, []);

  const dropDownOptions = useMemo(
    () =>
      routes.map((r, index) => ({
        label: `${index}. score: ${r.score} | ${r.molecule.name}`,
        index: index,
      })),
    [routes]
  );

  const isReadyToDisplayTree =
    !isLoading && (selectedRouteIndex || selectedRouteIndex === 0);
  const selectedRoute = isReadyToDisplayTree && routes[selectedRouteIndex];

  const node = ({ nodeDatum, toggleNode }) => {
    const smiles = nodeDatum.name;
    return (
      // TODO: Make this to show the molecule on hover.
      <g>
        <ReactSVG
          src={encodeURI(
            `http://localhost:8000/molecule?smiles=${smiles}&height=${NODE_HIGHT}&width=${NODE_WIDTH}`
          )}
          onClick={toggleNode}
          wrapper="svg"
          aria-label={smiles}
        />
      </g>
    );
  };

  const pathFunc = (linkData, orientation) => {
    const { source, target } = linkData;
    return `M${source.y + NODE_HIGHT},${source.x + NODE_WIDTH / 2}L${
      target.y + NODE_HIGHT / 2
    },${target.x + NODE_WIDTH / 2}`;
  };

  return (
    !isLoading && (
      <>
        <Autocomplete
          disablePortal
          options={dropDownOptions}
          sx={{ width: 600 }}
          renderInput={(params) => <TextField {...params} label="Molecule" />}
          onChange={(_, v) => setSelectedRouteIndex(v.index)}
        />
        {isReadyToDisplayTree && (
          <Card>
            <CardContent sx={{ minWidth: "30vw", height: "60vw" }}>
              <Typography gutterBottom variant="h5" component="div">
                {selectedRoute?.molecule?.name} Score: {selectedRoute?.score}
              </Typography>
              (
              <Tree
                key={selectedRouteIndex}
                data={selectedRoute?.molecule}
                orientation="horizontal"
                translate={{ x: NODE_WIDTH, y: NODE_HIGHT }}
                nodeSize={{ x: 2 * NODE_WIDTH, y: 2 * NODE_HIGHT }}
                renderCustomNodeElement={node}
                pathFunc={pathFunc}
              />
              )
            </CardContent>
          </Card>
        )}
      </>
    )
  );
};
