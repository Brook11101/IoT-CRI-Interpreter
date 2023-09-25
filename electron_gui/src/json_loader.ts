import { readdirSync, readFileSync, statSync } from "fs";
import { join } from "path";

export function getFilenamesInDirectory(directoryPath: string): string[] {
  let fileNames = readdirSync(directoryPath);

  fileNames = fileNames.filter((fileName) => {
    return statSync(join(directoryPath, fileName)).isFile();
  });

  return fileNames;
}

export function readJsonFile(filePath: string): any {
  const fileContent = readFileSync(filePath, "utf-8");
  return JSON.parse(fileContent);
}

export function searchModuleName(json_content: Object, name: string) {
  for (let item of Object.values(json_content)) {
    if (item["name"] == name) {
      return item["module_name"];
    }
  }
  return "";
}
