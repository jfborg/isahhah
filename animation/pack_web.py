"""Serve model textures as ordinary same-origin files, avoiding blob URL loaders."""
import json,struct,re
from pathlib import Path

def pack(path):
 path=Path(path);raw=path.read_bytes();n=struct.unpack_from('<I',raw,12)[0]
 doc=json.loads(raw[20:20+n]);start=20+n;length=struct.unpack_from('<I',raw,start)[0];binary=raw[start+8:start+8+length]
 images=doc.get('images',[])
 if not any('bufferView'in im for im in images):return
 folder=path.parent/'textures';folder.mkdir(exist_ok=True)
 excluded=set()
 for i,im in enumerate(images):
  view=im.get('bufferView')
  if view is None:continue
  data=doc['bufferViews'][view];offset=data.get('byteOffset',0)
  suffix='.jpg' if im.get('mimeType')=='image/jpeg' else '.png'
  name=re.sub(r'[^a-zA-Z0-9_-]','_',im.get('name',f'texture-{i}'))+suffix
  (folder/name).write_bytes(binary[offset:offset+data['byteLength']]);excluded.add(view)
  im.pop('bufferView');im.pop('mimeType',None);im['uri']='textures/'+name
 views=[];payload=bytearray();mapping={}
 for i,view in enumerate(doc['bufferViews']):
  if i in excluded:continue
  while len(payload)%4:payload.append(0)
  old=view.get('byteOffset',0);updated=dict(view);updated['byteOffset']=len(payload)
  payload.extend(binary[old:old+view['byteLength']]);mapping[i]=len(views);views.append(updated)
 def remap(value):
  if isinstance(value,dict):
   for k,v in value.items():
    if k=='bufferView':value[k]=mapping[v]
    else:remap(v)
  elif isinstance(value,list):
   for v in value:remap(v)
 remap(doc);doc['bufferViews']=views
 while len(payload)%4:payload.append(0)
 doc['buffers'][0]['byteLength']=len(payload)
 text=json.dumps(doc,separators=(',',':')).encode()
 text+=b' '*((-len(text))%4)
 total=12+8+len(text)+8+len(payload)
 path.write_bytes(struct.pack('<III',0x46546c67,2,total)+struct.pack('<II',len(text),0x4e4f534a)+text+struct.pack('<II',len(payload),0x004e4942)+payload)
 print('WEB_MODEL_READY',len(images),'external textures',path.stat().st_size,'model bytes')

if __name__=='__main__':pack(Path(__file__).resolve().parent.parent/'public/media/3d/instructor.glb')
