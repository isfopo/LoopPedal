import { arc, circle } from "@jscad/modeling/src/primitives";
import { extrudeLinear } from "@jscad/modeling/src/operations/extrusions";
import { expand } from "@jscad/modeling/src/operations/expansions";
import convert from "convert";

const rod = {
  length: convert(2, "ft").to("mm"),
  diameter: convert(3 / 4, "in").to("mm"),
  nut: {
    height: convert(1 / 2, "in").to("mm"),
    clearance: convert(1, "in").to("mm"),
  },
};

const section = {
  width: rod.length / 4,
};

const buttons = {
  diameter: convert(1 / 2, "in").to("mm"),
  count: 8,
};

const dimensions = {
  face: convert(3, "in").to("mm"),
  back: convert(3 / 2, "in").to("mm"),
  angle: convert(80, "deg").to("rad"),
  thickness: convert(1 / 32, "in").to("mm"),
};

const body = () => {
  return extrudeLinear(
    { height: section.width },
    expand({ delta: dimensions.thickness }, arc({ radius: rod.diameter / 2 }))
  );
};

export const main = () => {
  return body();
};
