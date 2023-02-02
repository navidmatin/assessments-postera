import React, { useEffect, useState, useMemo, useCallback } from "react";

import { Autocomplete, TextField } from "@mui/material";
import { MoleculeTree } from "./MoleculeTree";

export const Routes = () => {
  const [routes, setRoutes] = useState([]);
  const [selectedRouteIndex, setSelectedRouteIndex] = useState(null);
  const [isLoading, setLoading] = useState(true);
  const [smilesToAttr, setSmilesToAttr] = React.useState();

  const fetchRoutes = async () => {
    const response = await fetch("http://localhost:8000/routes");
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

  const onDropDownChange = (_, v) => {
    setSelectedRouteIndex(v?.index);
  };

  return (
    !isLoading && (
      <>
        <Autocomplete
          disablePortal
          options={dropDownOptions}
          sx={{ width: 600 }}
          renderInput={(params) => <TextField {...params} label="Molecule" />}
          onChange={onDropDownChange}
        />
        {isReadyToDisplayTree && (
          <MoleculeTree
            smilesToAttrMap={smilesToAttr}
            route={selectedRoute}
            routeId={selectedRouteIndex}
          />
        )}
      </>
    )
  );
};
