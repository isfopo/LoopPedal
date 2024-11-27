import { arc, circle, line } from "@jscad/modeling/src/primitives";
import { extrudeLinear } from "@jscad/modeling/src/operations/extrusions";
import { expand } from "@jscad/modeling/src/operations/expansions";
import { union } from "@jscad/modeling/src/operations/booleans";
import convert from "convert";

interface SectionOptions {
  isEndSection: boolean;
}

const rod = {
  length: convert(2, "ft").to("mm"),
  diameter: convert(1 / 2, "in").to("mm"),
  nut: {
    height: convert(1 / 2, "in").to("mm"),
  },
};

const section = {
  width: (isEndSection: boolean = false) =>
    (rod.length - (isEndSection ? rod.nut.height : 0)) / 4,
};

const buttons = {
  diameter: convert(1 / 2, "in").to("mm"),
  count: 8,
};

const dimensions = {
  face: convert(3, "in").to("mm"),
  back: convert(3 / 2, "in").to("mm"),
  angle: convert(80, "deg").to("rad"),
  thickness: convert(1 / 16, "in").to("mm"),
};

const sectionGeo = ({ isEndSection }: SectionOptions) => {
  const shafts = [
    arc({ radius: rod.diameter / 2 + dimensions.thickness / 2 }),
    arc({
      radius: rod.diameter / 2 + dimensions.thickness / 2,
      center: [0, dimensions.face],
    }),
    arc({
      radius: rod.diameter / 2 + dimensions.thickness / 2,
      center: [-dimensions.back, 0],
    }),
  ];

  const face = line([
    [rod.diameter / 2 + dimensions.thickness / 2, dimensions.face],
    [rod.diameter / 2 + dimensions.thickness / 2, 0],
  ]);

  const back = line([
    [-dimensions.back, -(rod.diameter / 2 + dimensions.thickness / 2)],
    [0, -(rod.diameter / 2 + dimensions.thickness / 2)],
  ]);

  return extrudeLinear(
    { height: section.width(isEndSection) },
    expand({ delta: dimensions.thickness }, ...shafts, face, back)
  );
};

export const main = () => {
  return sectionGeo({ isEndSection: true });
};
