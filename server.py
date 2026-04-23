"""PSA Advocacia — Backend v2 (Render.com ready)"""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import httpx, json, os, re

app = FastAPI(title="PSA Advocacia v2")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "database.json")

DEFAULT_DB = {
    "proc": [
        {"id":1,"num":"0837052-73.2025.8.19.0209","area":"FAMILIA","autor":"JULIANE LIMA RANGEL","reu":"ESPÓLIO DE RODOLFO PORTILHO DE LIMA / BALIEIRA / DULCEMAR PORTILHO DE LIMA","forum":"2ª Vara de Família da Regional da Barra da Tijuca","modal":"PROCESSO PRINCIPAL","sistema":"ONLINEPJE","status":"PENDENTE","valor":"R$1.000,00","custom":{}},
        {"id":2,"num":"0842819-37.2025.8.19.0001","area":"CRIMINAL","autor":"DULCEMAR PORTILHO DE LIMA","reu":"RIO DE JANEIRO SECRETARIA DE EST. DE SEGURANCA PUBLICA","forum":"19ª Vara Criminal da Comarca da Capital","modal":"DESDOBRAMENTO","sistema":"ONLINEPJE","status":"EM ANDAMENTO","valor":"R$0,00","custom":{}},
        {"id":3,"num":"0800198-80.2025.8.19.0209","area":"INVENTARIO","autor":"DULCEMAR PORTILHO DE LIMA","reu":"ESPÓLIO DE RODOLFO PORTILHO DE LIMA / BALIEIRA / DULCEMAR PORTILHO DE LIMA","forum":"3ª Vara de Família da Regional da Barra da Tijuca","modal":"DESDOBRAMENTO","sistema":"ONLINEPJE","status":"EM ANDAMENTO","valor":"R$50.000,00","custom":{}},
        {"id":4,"num":"REGISTRO DE OCORRÊNCIA 016-24597/2024","area":"CRIMINAL","autor":"JULIANE LIMA RANGEL","reu":"DULCEMAR PORTILHO DE LIMA","forum":"16ª Delegacia de Polícia Civil do Estado do Rio de Janeiro","modal":"DESDOBRAMENTO","sistema":"AREA RESTRITA - OAB/RJ","status":"FINALIZADO","valor":"R$0,00","custom":{}},
        {"id":5,"num":"0805429-25.2024.8.19.0209","area":"FAMILIA","autor":"AMANDA MARISTELA LOIOLA GUIMARAES","reu":"TITTO VITO LOIOLA GUIMARÃES GALVÃO","forum":"3ª Vara de Família da Regional da Barra da Tijuca","modal":"DESDOBRAMENTO","sistema":"ONLINEPJE","status":"EM ANDAMENTO","valor":"R$1.000,00","custom":{}},
        {"id":6,"num":"5097923-29.2024.4.02.5101","area":"PREVIDENCIARIO","autor":"RODOLFO PORTILHO DE LIMA BALIEIRA","reu":"INSTITUTO NACIONAL DO SEGURO SOCIAL","forum":"40ª Vara Federal do Rio de Janeiro","modal":"DESDOBRAMENTO","sistema":"JUSTIÇA FEDERAL 2ª REGIÃO","status":"PENDENTE","valor":"R$10.000,00","custom":{}},
        {"id":7,"num":"0002125-97.2026.8.05.0103","area":"TRABALHISTA","autor":"MOBILY PETS LTDA","reu":"NADINE BATISTA DOS SANTOS","forum":"","modal":"PROCESSO PRINCIPAL","sistema":"ONLINEPJE","status":"EM ANDAMENTO","valor":"R$0,00","custom":{}},
        {"id":8,"num":"006770-88.2026.8.17.8201","area":"TRABALHISTA","autor":"MARIA JACIRA RODRIGUES DE QUARESMA","reu":"MOBILY PETS LTDA","forum":"","modal":"PROCESSO PRINCIPAL","sistema":"ONLINEPJE","status":"EM ANDAMENTO","valor":"R$0,00","custom":{}},
    ],
    "and": [
        {"id":1,"procId":2,"data":"2025-12-11","tipo":"Decisão","resp":"Dr. PSA","desc":"A 19ª Vara Criminal determinou remessa dos autos ao TJRJ para apreciação da gratuidade de justiça."},
        {"id":2,"procId":3,"data":"2026-02-20","tipo":"Consulta PJe","resp":"Dr. PSA","desc":"Consulta realizada no PJe em 20/02/2026."},
        {"id":3,"procId":4,"data":"2024-12-01","tipo":"Resposta OAB","resp":"Dr. PSA","desc":"Solicitação deferida via convênio OAB/RJ. Protocolar no SESOP."},
        {"id":4,"procId":5,"data":"2025-04-01","tipo":"Juntada","resp":"Dr. PSA","desc":"Juntada de Petição de Manifestação do MPRJ."},
        {"id":5,"procId":6,"data":"2025-09-16","tipo":"Petição","resp":"Dr. PSA","desc":"16/09/2025 — PETIÇÃO — Refer. ao Evento 14."},
    ],
    "tar": [
        {"id":1,"titulo":"Consultar andamento processo família Juliane","procId":1,"resp":"Dr. PSA","prazo":"2025-05-15","prio":"Alta","status":"Pendente","obs":""},
        {"id":2,"titulo":"Preparar petição mandado de segurança","procId":2,"resp":"Dr. PSA","prazo":"2025-05-20","prio":"Alta","status":"Em Andamento","obs":""},
        {"id":3,"titulo":"Revisar inventário — documentos pendentes","procId":3,"resp":"Dr. PSA","prazo":"2025-06-01","prio":"Média","status":"Pendente","obs":""},
        {"id":4,"titulo":"Contato com cliente INSS","procId":6,"resp":"Dr. PSA","prazo":"2025-05-30","prio":"Baixa","status":"Aguardando Retorno","obs":""},
    ],
    "cli": [
        {"id":1,"nome":"JULIANE LIMA RANGEL","tipo":"PF","doc":"","tel":"","email":"","end":"Rio de Janeiro - RJ","nasc":"","obs":"Autora processo família e ocorrência criminal.","custom":{}},
        {"id":2,"nome":"DULCEMAR PORTILHO DE LIMA","tipo":"PF","doc":"","tel":"","email":"","end":"Rio de Janeiro - RJ","nasc":"","obs":"Autora mandado de segurança e inventário.","custom":{}},
        {"id":3,"nome":"AMANDA MARISTELA LOIOLA GUIMARAES","tipo":"PF","doc":"","tel":"","email":"","end":"Rio de Janeiro - RJ","nasc":"","obs":"Ação de família na 3ª Vara.","custom":{}},
        {"id":4,"nome":"RODOLFO PORTILHO DE LIMA BALIEIRA","tipo":"PF","doc":"","tel":"","email":"","end":"Rio de Janeiro - RJ","nasc":"","obs":"Ação previdenciária contra INSS.","custom":{}},
        {"id":5,"nome":"MOBILY PETS LTDA","tipo":"PJ","doc":"51.327.049/0001-94","tel":"(21) 7932-6339","email":"mobilypetsadm@gmail.com","end":"","nasc":"","obs":"2 processos trabalhistas ativos.","custom":{}},
    ],
    "eventos": [
        {"id":1,"procId":1,"tipo":"prazo","titulo":"Prazo para manifestação","data":"2025-05-10","hora":"23:59","descricao":"Prazo fatal para petição","notificar":True,"notificadoDias":3,"cor":"#e07070"},
        {"id":2,"procId":2,"tipo":"audiencia","titulo":"Audiência de instrução","data":"2025-05-20","hora":"14:00","descricao":"19ª Vara Criminal","notificar":True,"notificadoDias":2,"cor":"#8ab0e0"},
        {"id":3,"procId":5,"tipo":"audiencia","titulo":"Audiência de conciliação","data":"2025-06-05","hora":"10:30","descricao":"3ª Vara de Família","notificar":True,"notificadoDias":2,"cor":"#d080b0"},
        {"id":4,"procId":6,"tipo":"prazo","titulo":"Prazo recursal INSS","data":"2025-06-15","hora":"23:59","descricao":"TRF 2ª Região","notificar":True,"notificadoDias":5,"cor":"#70b0e0"},
        {"id":5,"procId":3,"tipo":"reuniao","titulo":"Reunião com cliente — inventário","data":"2025-05-08","hora":"16:00","descricao":"Escritório","notificar":True,"notificadoDias":1,"cor":"#c9a84c"},
    ],
    "demandas": [
        {"id":1,"titulo":"Regularização documental — Espólio Portilho","procId":3,"status":"Em Andamento","prioridade":"Alta","responsavel":"Dr. PSA","descricao":"Regularizar documentação do espólio.","etapas":[{"id":1,"texto":"Levantar certidões","feito":True},{"id":2,"texto":"Protocolar habilitação","feito":False},{"id":3,"texto":"Aguardar homologação","feito":False}],"dataInicio":"2025-04-01","dataPrazo":"2025-07-01","progresso":33},
        {"id":2,"titulo":"Recurso INSS — Coleta de documentos","procId":6,"status":"Pendente","prioridade":"Alta","responsavel":"Dr. PSA","descricao":"Coletar laudos médicos e histórico previdenciário.","etapas":[{"id":1,"texto":"Solicitar laudos ao cliente","feito":False},{"id":2,"texto":"Organizar documentos","feito":False},{"id":3,"texto":"Protocolar recurso","feito":False}],"dataInicio":"2025-04-10","dataPrazo":"2025-06-15","progresso":0},
        {"id":3,"titulo":"Mobily Pets — Defesa trabalhista Nadine","procId":7,"status":"Em Andamento","prioridade":"Alta","responsavel":"Dr. PSA","descricao":"Defesa no processo trabalhista movido por Nadine Batista dos Santos.","etapas":[{"id":1,"texto":"Coletar documentos da empresa","feito":False},{"id":2,"texto":"Elaborar contestação","feito":False},{"id":3,"texto":"Protocolar defesa","feito":False},{"id":4,"texto":"Acompanhar audiência","feito":False}],"dataInicio":"2026-04-01","dataPrazo":"","progresso":0},
        {"id":4,"titulo":"Mobily Pets — Defesa trabalhista Maria Jacira","procId":8,"status":"Em Andamento","prioridade":"Alta","responsavel":"Dr. PSA","descricao":"Defesa no processo trabalhista movido por Maria Jacira Rodrigues de Quaresma.","etapas":[{"id":1,"texto":"Coletar documentos da empresa","feito":False},{"id":2,"texto":"Elaborar contestação","feito":False},{"id":3,"texto":"Protocolar defesa","feito":False},{"id":4,"texto":"Acompanhar audiência","feito":False}],"dataInicio":"2026-04-01","dataPrazo":"","progresso":0},
    ],
    "campos": {"proc":[],"cli":[]},
    "next_id": {"proc":9,"and":6,"tar":5,"cli":6,"evento":6,"demanda":5},
}

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE,"r",encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return json.loads(json.dumps(DEFAULT_DB))

def save_db(db):
    try:
        with open(DB_FILE,"w",encoding="utf-8") as f:
            json.dump(db,f,ensure_ascii=False,indent=2)
    except Exception as e:
        print(f"Aviso: não foi possível salvar: {e}")

class Processo(BaseModel):
    num:str; area:str; autor:str; reu:Optional[str]=""; forum:Optional[str]=""
    modal:Optional[str]="PROCESSO PRINCIPAL"; sistema:Optional[str]="ONLINEPJE"
    status:Optional[str]="ATIVOS"; valor:Optional[str]=""; custom:Optional[dict]={}

class Andamento(BaseModel):
    procId:int; data:str; tipo:str; resp:Optional[str]=""; desc:Optional[str]=""

class Tarefa(BaseModel):
    titulo:str; procId:Optional[int]=None; resp:Optional[str]=""
    prazo:Optional[str]=""; prio:Optional[str]="Média"; status:Optional[str]="Pendente"; obs:Optional[str]=""

class Cliente(BaseModel):
    nome:str; tipo:Optional[str]="PF"; doc:Optional[str]=""; tel:Optional[str]=""
    email:Optional[str]=""; end:Optional[str]=""; nasc:Optional[str]=""; obs:Optional[str]=""; custom:Optional[dict]={}

class Evento(BaseModel):
    procId:Optional[int]=None; tipo:str; titulo:str; data:str; hora:Optional[str]="09:00"
    descricao:Optional[str]=""; notificar:Optional[bool]=True; notificadoDias:Optional[int]=1; cor:Optional[str]="#c9a84c"

class EtapaModel(BaseModel):
    id:int; texto:str; feito:bool

class Demanda(BaseModel):
    titulo:str; procId:Optional[int]=None; status:Optional[str]="Pendente"; prioridade:Optional[str]="Média"
    responsavel:Optional[str]=""; descricao:Optional[str]=""; etapas:Optional[List[EtapaModel]]=[]
    dataInicio:Optional[str]=""; dataPrazo:Optional[str]=""; progresso:Optional[int]=0

class Campo(BaseModel):
    entity:str; nome:str; tipo:str; opcoes:Optional[List[str]]=[]

@app.get("/api/db")
def get_db():
    return load_db()

NK = {"proc":"proc","and":"and","tar":"tar","cli":"cli","eventos":"evento","demandas":"demanda"}

def make_crud(entity, ModelClass, path):
    nk = NK.get(entity, entity[:3])
    @app.get(f"/api/{path}", name=f"list_{entity}")
    def list_all(): return load_db()[entity]
    @app.post(f"/api/{path}", name=f"create_{entity}")
    def create(obj: ModelClass):
        db=load_db(); id=db["next_id"][nk]; db["next_id"][nk]+=1
        db[entity].append({"id":id,**obj.dict()}); save_db(db); return {"id":id,"ok":True}
    @app.put(f"/api/{path}/{{id}}", name=f"update_{entity}")
    def update(id:int, obj:ModelClass):
        db=load_db()
        for i,x in enumerate(db[entity]):
            if x["id"]==id: db[entity][i]={"id":id,**obj.dict()}; save_db(db); return {"ok":True}
        raise HTTPException(404)
    @app.delete(f"/api/{path}/{{id}}", name=f"delete_{entity}")
    def delete(id:int):
        db=load_db(); db[entity]=[x for x in db[entity] if x["id"]!=id]; save_db(db); return {"ok":True}

for e,m,p in [("proc",Processo,"proc"),("and",Andamento,"and"),("tar",Tarefa,"tar"),("cli",Cliente,"cli"),("eventos",Evento,"eventos"),("demandas",Demanda,"demandas")]:
    make_crud(e,m,p)

@app.post("/api/campo")
def create_campo(c:Campo):
    db=load_db(); db["campos"][c.entity].append({"nome":c.nome,"tipo":c.tipo,"opcoes":c.opcoes}); save_db(db); return {"ok":True}

@app.delete("/api/campo/{entity}/{idx}")
def delete_campo(entity:str, idx:int):
    db=load_db(); db["campos"][entity].pop(idx); save_db(db); return {"ok":True}

TRIBUNAL_MAP={"8.19":"tjrj","8.26":"tjsp","8.07":"tjdft","8.13":"tjmg","8.21":"tjrs","4.02":"trf2","4.03":"trf3","4.01":"trf1","4.04":"trf4","4.05":"trf5","5.01":"tst"}

def extrair_tribunal(numero):
    m=re.search(r'\d{7}-\d{2}\.\d{4}\.(\d\.\d{2})\.\d{4}',numero)
    return TRIBUNAL_MAP.get(m.group(1)) if m else None

async def buscar_datajud(numero):
    tribunal=extrair_tribunal(numero)
    if not tribunal: return {"erro":"Número não reconhecido."}
    url=f"https://api-publica.datajud.cnj.jus.br/api_publica_{tribunal}/_search"
    headers={"Authorization":"ApiKey cDZHYzlZa0JadVREZDJCendFbGFDdmQ6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==","Content-Type":"application/json"}
    try:
        async with httpx.AsyncClient(timeout=15.0) as c:
            r=await c.post(url,json={"query":{"match":{"numeroProcesso":numero}}},headers=headers)
            if r.status_code!=200: return {"erro":f"Status {r.status_code}"}
            hits=r.json().get("hits",{}).get("hits",[])
            if not hits: return {"erro":f"Processo não encontrado ({tribunal.upper()})."}
            return {"tribunal":tribunal.upper(),"dados":hits[0].get("_source",{})}
    except Exception as e: return {"erro":str(e)}

@app.get("/api/cnj/{numero:path}")
async def consultar_cnj(numero:str):
    r=await buscar_datajud(numero)
    if "erro" in r: return JSONResponse(status_code=400,content=r)
    d=r["dados"]
    movs=[{"data":m.get("dataHora","")[:10],"tipo":m.get("nome",""),"complemento":(m.get("complementosTabelados") or [{}])[0].get("descricao","")} for m in d.get("movimentos",[])[:20]]
    return {"tribunal":r["tribunal"],"numero":d.get("numeroProcesso",numero),"classe":d.get("classe",{}).get("nome",""),"assunto":", ".join(a.get("nome","") for a in d.get("assuntos",[])),"dataAjuizamento":d.get("dataAjuizamento","")[:10] if d.get("dataAjuizamento") else "","grau":d.get("grau",""),"orgaoJulgador":d.get("orgaoJulgador",{}).get("nome",""),"movimentos":movs,"partes":[{"nome":p.get("nome",""),"polo":p.get("polo","")} for p in d.get("partes",[])]}

app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/")
def index(): return FileResponse("static/index.html")

@app.get("/{full_path:path}")
def catch_all(full_path:str): return FileResponse("static/index.html")

if __name__=="__main__":
    import uvicorn
    port=int(os.environ.get("PORT",8000))
    print(f"\n{'='*50}\n  PSA Advocacia v2 — http://localhost:{port}\n{'='*50}\n")
    uvicorn.run("server:app",host="0.0.0.0",port=port,reload=False)
