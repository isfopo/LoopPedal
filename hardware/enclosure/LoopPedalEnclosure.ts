import { arc, circle, cylinder, line } from "@jscad/modeling/src/primitives";
import { extrudeLinear } from "@jscad/modeling/src/operations/extrusions";
import { expand } from "@jscad/modeling/src/operations/expansions";
import { subtract, union } from "@jscad/modeling/src/operations/booleans";
import { rotate, translate } from "@jscad/modeling/src/operations/transforms";
import convert from "convert";

interface SectionOptions {
  isEndSection: "left" | "right" | undefined;
  hasPort: boolean;
}

const rod = {
  length: convert(2, "ft").to("mm"),
  diameter: convert(1 / 2, "in").to("mm"),
  nut: {
    height: convert(1 / 2, "in").to("mm"),
  },
};

const section = {
  /** Width of each section */
  width: rod.length / 4,
  /** Accounts for the length of the nut */
  adjustedWidth: (isEndSection: "left" | "right" | undefined) =>
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
  thickness: convert(3 / 16, "in").to("mm"),
};

const sectionGeo = ({ isEndSection }: SectionOptions) => {
  const offsetRadius = rod.diameter / 2 + dimensions.thickness / 2;

  const shafts = (inner?: boolean) => [
    circle({ radius: inner ? rod.diameter / 2 : offsetRadius }),
    circle({
      radius: inner ? rod.diameter / 2 : offsetRadius,
      center: [0, dimensions.face],
    }),
    circle({
      radius: inner ? rod.diameter / 2 : offsetRadius,
      center: [-dimensions.back, 0],
    }),
  ];

  const face = line([
    [offsetRadius, dimensions.face],
    [offsetRadius, 0],
  ]);

  const back = line([
    [-dimensions.back, -offsetRadius],
    [0, -offsetRadius],
  ]);

  const buttonGeo = (i: number) =>
    cylinder({
      radius: buttons.diameter / 2,
      height: dimensions.thickness * 2,
      center: [
        i * (section.width / buttons.countPerSection) -
          (isEndSection === "right" ? rod.nut.height / 2 : 0),
        dimensions.face / 2,
        0,
      ],
    });

  const buttonsGeo = rotate(
    [0, -Math.PI / 2, 0],
    translate(
      [-section.width / buttons.countPerSection / 2, 0, -offsetRadius],
      buttonGeo(1),
      buttonGeo(2)
    )
  );

  return subtract(
    union(
      extrudeLinear(
        { height: section.adjustedWidth(isEndSection) },
        subtract(
          union(
            expand({ delta: dimensions.thickness }, ...shafts(), face, back)
          ),
          ...shafts(true)
        )
      )
    ),
    buttonsGeo
  );
};

export const main = () => {
  return sectionGeo({ isEndSection: "right", hasPort: true });
};
