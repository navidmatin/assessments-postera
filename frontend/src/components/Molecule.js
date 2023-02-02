import React, { useEffect, useState, useMemo } from "react";
import { ReactSVG } from "react-svg";

export const Molecule = ({ data, onToggle }) => {
  const smiles = data.name;
  return (
    <ReactSVG
      src={encodeURI(`http://localhost:8000/molecule?smiles=${smiles}`)}
      onClick={onToggle}
      wrapper="svg"
    />
  );
};
