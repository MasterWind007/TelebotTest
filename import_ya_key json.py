import json
from pathlib import Path
yandexKey = {'OAuth':'y0_AgAAAAA2GPPIAATuwQAAAADeYXG_MunkevKMS_GIRQsbKNqepm-n3wg',
              'folderid':'b1g9m7ogbnpo0afrth9g'}
with open(Path('Comon','Res','yaKEY.json'),'w') as f:
    json.dump(yandexKey, f,  sort_keys=True, indent=2)
