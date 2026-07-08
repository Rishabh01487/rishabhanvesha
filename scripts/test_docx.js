const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, PageNumber, TableOfContents, PageBreak } = require("docx");
const fs = require("fs");

const doc = new Document({
  sections: [
    { properties: { page: { margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 } } },
      children: [
        new Paragraph({ text: "Cover", alignment: AlignmentType.CENTER, children: [new TextRun("Cover")] }),
        new Paragraph({ children: [new PageBreak()] }),
        new Paragraph({ text: "Chapter 1", heading: HeadingLevel.HEADING_1, children: [new TextRun("Chapter 1")] }),
        new Paragraph("Body text"),
      ],
    },
  ],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync("/home/z/my-project/download/test.docx", buf); console.log("OK"); });
