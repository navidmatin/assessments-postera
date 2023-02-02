import React, { useEffect, useState, useMemo, useCallback } from "react";
import { ReactSVG } from "react-svg";
import Tree from "react-d3-tree";
import ScienceIcon from "@mui/icons-material/Science";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";

import {
  Alert,
  AlertTitle,
  Autocomplete,
  Card,
  CardContent,
  Chip,
  Popover,
  TextField,
  Typography,
} from "@mui/material";
import { Stack } from "@mui/system";

export const Routes = () => {
  const [routes, setRoutes] = useState([]);
  const [selectedRouteIndex, setSelectedRouteIndex] = useState(null);
  const [isLoading, setLoading] = useState(true);

  const [popoverAnchor, setPopOverAnchor] = React.useState();
  const [popOverSmiles, setPopOverSmiles] = React.useState();
  const [smilesToAttr, setSmilesToAttr] = React.useState();

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

  const createSmileToAttributesMap = useCallback((route) => {
    if (!route?.children) {
      return null;
    }
    let smilesToAttrMap = new Map();
    route.children.forEach(
      (child) =>
        (smilesToAttrMap = new Map([
          ...createSmileToAttributesMap(child),
          ...smilesToAttrMap,
        ]))
    );
    smilesToAttrMap.set(route.name, route.attributes);

    return smilesToAttrMap;
  }, []);

  const isOpen = !!popoverAnchor;
  const isReadyToDisplayTree =
    !isLoading && (selectedRouteIndex || selectedRouteIndex === 0);
  const selectedRoute = isReadyToDisplayTree && routes[selectedRouteIndex];

  useEffect(() => {
    const route = isReadyToDisplayTree && routes[selectedRouteIndex];
    setSmilesToAttr(createSmileToAttributesMap(route?.molecule));
  }, [
    createSmileToAttributesMap,
    selectedRouteIndex,
    routes,
    isReadyToDisplayTree,
  ]);

  const handlePopoverOpen = (event) => {
    const { smiles } = event.target.dataset;
    setPopOverAnchor(event.currentTarget);
    setPopOverSmiles(smiles);
  };

  const handlePopoverClose = () => {
    setPopOverAnchor(null);
  };

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

  const pathFunc = (linkData, _) => {
    const { source, target } = linkData;
    return `M${source.y + NODE_HIGHT},${source.x + NODE_WIDTH / 2}L${
      target.y + NODE_HIGHT / 2
    },${target.x + NODE_WIDTH / 2}`;
  };

  const popOverAttributes = smilesToAttr?.get(popOverSmiles);
  const popOverReactions = popOverAttributes?.reactions;
  const popOverCatalogs = popOverAttributes?.acquisition_catalogs;

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
                  {popOverReactions?.length > 0 && (
                    <>
                      <Chip icon={<ScienceIcon />} label={popOverReactions} />
                    </>
                  )}
                  <Stack spacing={1}>
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
        )}
      </>
    )
  );
};
