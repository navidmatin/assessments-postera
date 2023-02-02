import React, { useState, useCallback } from "react";
import { ReactSVG } from "react-svg";
import Tree from "react-d3-tree";
import ScienceIcon from "@mui/icons-material/Science";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";

import {
  Alert,
  AlertTitle,
  Card,
  CardContent,
  Chip,
  Popover,
  Stack,
  Typography,
} from "@mui/material";

const NODE_HIGHT = 200;
const NODE_WIDTH = 200;

export const MoleculeTree = ({ smilesToAttrMap, route }) => {
  const [popoverAnchor, setPopOverAnchor] = useState();
  const [popOverSmiles, setPopOverSmiles] = useState();

  const handlePopoverOpen = (event) => {
    const { smiles } = event.target.dataset;
    setPopOverAnchor(event.currentTarget);
    setPopOverSmiles(smiles);
  };

  const handlePopoverClose = () => {
    setPopOverAnchor(null);
  };

  const pathFunc = (linkData, _) => {
    const { source, target } = linkData;
    return `M${source.y + NODE_HIGHT},${source.x + NODE_WIDTH / 2}L${
      target.y + NODE_HIGHT / 2
    },${target.x + NODE_WIDTH / 2}`;
  };

  const isOpen = !!popoverAnchor;
  const node = useCallback(({ nodeDatum, toggleNode }) => {
    const smiles = nodeDatum.name;
    return (
      <>
        <ReactSVG
          src={encodeURI(
            `http://localhost:8000/molecule?smiles=${smiles}&height=${NODE_HIGHT}&width=${NODE_WIDTH}`
          )}
          onClick={toggleNode}
          wrapper="svg"
          aria-label={smiles}
          onMouseLeave={handlePopoverClose}
          data-smiles={smiles}
          onMouseEnter={handlePopoverOpen}
        />
      </>
    );
  }, []);

  const popOverAttributes = smilesToAttrMap?.get(popOverSmiles);
  const popOverReactions = popOverAttributes?.reactions;
  const popOverCatalogs = popOverAttributes?.acquisition_catalogs;

  return (
    <Card>
      <CardContent sx={{ minWidth: "30vw", height: "60vw" }}>
        <Typography gutterBottom variant="h5" component="div">
          {route?.molecule?.name} Score: {route?.score}
        </Typography>
        (
        <Tree
          data={route?.molecule}
          orientation="horizontal"
          translate={{ x: NODE_WIDTH, y: NODE_HIGHT }}
          nodeSize={{ x: 2 * NODE_WIDTH, y: 2 * NODE_HIGHT }}
          renderCustomNodeElement={node}
          pathFunc={pathFunc}
          onNodeMouseOver={handlePopoverOpen}
          onNodeMouseOut={handlePopoverClose}
        />
        <Popover
          open={isOpen}
          anchorEl={popoverAnchor}
          anchorOrigin={{
            vertical: "bottom",
            horizontal: "left",
          }}
          transformOrigin={{
            vertical: "top",
            horizontal: "left",
          }}
          onClose={handlePopoverClose}
          disableRestoreFocus
          sx={{
            pointerEvents: "none",
          }}
        >
          <Alert severity="info">
            <AlertTitle>{popOverSmiles}</AlertTitle>
            <Stack spacing={1} alignItems="flex-start">
              {popOverReactions?.length > 0 && (
                <>
                  <Chip icon={<ScienceIcon />} label={popOverReactions} />
                </>
              )}
              {popOverCatalogs?.map((catalog, i) => (
                <Chip
                  key={i}
                  icon={<ShoppingCartIcon />}
                  label={`${catalog.name} | ${catalog.lead_time_weeks} weeks lead time`}
                />
              ))}
            </Stack>
          </Alert>
        </Popover>
        )
      </CardContent>
    </Card>
  );
};
