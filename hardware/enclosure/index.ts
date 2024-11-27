import { cube } from "@jscad/modeling/src/primitives";
import convert from "convert";

const rod = {
  length: convert(2, "ft").to("mm"),
  diameter: convert(3 / 4, "in").to("mm"),
  nut: {
    height: convert(1 / 2, "in").to("mm"),
    clearance: convert(1, "in").to("mm"),
  },
};

const buttons = {
  diameter: convert(1 / 2, "in").to("mm"),
  count: 8,
};

const dimensions = {
  face: convert(3, "in").to("mm"),
  back: convert(3 / 2, "in").to("mm"),
  angle: convert(45, "deg").to("rad"),
  thickness: convert(1 / 4, "in").to("mm"),
};

export const main = () => {
  return cube({ size: 20 });
};
