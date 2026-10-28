import json
from pathlib import Path
class jsonschema:
 @staticmethod
 def validate(value,schema):
  typ=schema.get('type')
  assert typ is None or isinstance(value,{'object':dict,'array':list,'string':str}[typ]),'Wrong type'
  if typ=='object':
   assert all(k in value for k in schema.get('required',[])),'Missing field'
   props=schema.get('properties',{})
   if schema.get('additionalProperties') is False: assert set(value)<=set(props),'Extra field'
   for k,v in value.items():
    if k in props: jsonschema.validate(v,props[k])
  if typ=='array':
   for v in value: jsonschema.validate(v,schema['items'])
r=Path(__file__).resolve().parents[3]
a=r/'agents/diffusion_agent'
schema=json.loads((r/'core/output_schema.json').read_text())
p,c,d=[json.loads((a/'responses'/f'{n}_response.json').read_text()) for n in ['primary','contrast_1','contrast_2']]
for name,x in zip(['primary','contrast_1','contrast_2'],[p,c,d]):
 jsonschema.validate(x,schema);print(name+': full output schema PASS')
for n in ['primary','contrast_1','contrast_2']:
 jsonschema.validate(json.loads((a/'cases'/f'{n}.json').read_text()),json.loads((r/'core/input_schema.json').read_text()))
print('Three input schemas PASS')
assert p['general_et_finding']==c['general_et_finding']==d['general_et_finding']
assert p['evidence']==c['evidence']==d['evidence']
assert p['application_finding']==c['application_finding']
assert p['application_finding']!=d['application_finding']
assert len({x['recommendation_management_implication'] for x in [p,c,d]})==3
for x in [p,c,d]:
 for f in ['relative advantage','compatibility','complexity','trialability','observability']:
  assert f in x['application_finding'].lower()
 assert x['abstention_or_more_information_needed']
print('Saved-artifact invariance, contrast, five-attribute and abstention checks PASS')
bad=json.loads((a/'records/diagnostic_failure_v0_response.json').read_text())
jsonschema.validate(bad,schema)
assert bad['general_et_finding']!=p['general_et_finding']
print('Negative control: schema passes; general evidence invariance FAILS as intended')
print('Manual review still required for source validity, reasoning, transfer and scope')
