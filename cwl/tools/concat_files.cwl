#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool

requirements:
  InlineJavascriptRequirement: {}  # to propagate the file format
  ResourceRequirement:
    coresMax: 1
    ramMin: 100  # just a default, could be lowered

inputs:
  files:
    type: File[]
    streamable: true
    inputBinding:
      position: 1
  outfile_name:
    type: string?
    default: result

baseCommand: cat

stdout: result  # to aid cwltool's cache feature

outputs:
  result:
    type: File
    outputBinding:
      glob: result
      outputEval: |
        ${ self[0].format = inputs.files[0].format;
           self[0].basename = inputs.outfile_name;
           return self;
         }


$namespaces:
  edam: http://edamontology.org/
  s: http://schema.org/
$schemas:
 - http://edamontology.org/EDAM_1.16.owl
 - https://schema.org/docs/schema_org_rdfa.html

s:license: "https://www.apache.org/licenses/LICENSE-2.0"
s:copyrightHolder: "EMBL - European Bioinformatics Institute"
