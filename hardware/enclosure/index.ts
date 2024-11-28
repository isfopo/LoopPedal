import { arc, circle, cylinder, line } from "@jscad/modeling/src/primitives";
import { extrudeLinear } from "@jscad/modeling/src/operations/extrusions";
import { expand } from "@jscad/modeling/src/operations/expansions";
import { subtract, union } from "@jscad/modeling/src/operations/booleans";
import { rotate, translate } from "@jscad/modeling/src/operations/transforms";
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
  countPerSection: 2,
};

const dimensions = {
  face: convert(4, "in").to("mm"),
  back: convert(2, "in").to("mm"),
  angle: convert(80, "deg").to("rad"),
  thickness: convert(3 / 32, "in").to("mm"),
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

  const buttonGeo = (i: number) =>
    cylinder({
      radius: buttons.diameter / 2,
      height: dimensions.thickness * 2,
      center: [
        i * (section.width(isEndSection) / buttons.countPerSection),
        dimensions.face / 2,
        0,
      ],
    });

  const buttonsGeo = rotate(
    [0, -Math.PI / 2, 0],
    translate(
      [
        -section.width(isEndSection) / buttons.countPerSection / 2,
        0,
        -(rod.diameter / 2 + dimensions.thickness / 2),
      ],
      buttonGeo(1),
      buttonGeo(2)
    )
  );

  return subtract(
    union(
      extrudeLinear(
        { height: section.width(isEndSection) },
        expand({ delta: dimensions.thickness }, ...shafts, face, back)
      )
    ),
    buttonsGeo
  );
};

export const main = () => {
  return sectionGeo({ isEndSection: true });
};
