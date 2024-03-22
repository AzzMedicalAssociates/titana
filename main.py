from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import importlib
import logging

app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)

class TextGenerationRequest(BaseModel):
    provider: str
    prompt: str

def process_task(request: TextGenerationRequest, task: str):
    global module
    provider_module = request.provider
    post_date = request.prompt
    logger.info(f"Processing task '{task}' with provider '{provider_module}'")

    try:
        provider_modules = {
            "Ahmad, S. Syed, MD": "Ahmad",
            "Albana, S. Fouad, MD": "Albana",
            "Anwar, F. Mohammad, MD": "Anwar",
            "Ashraf, Mohammad, M.D.": "Ashraf",
            "Bresch, David, MD": "Bresch",
            "Brown, Harold, MD": "Brown",
            "Chaudry, A. Ghazali, M.D.": "Chaudry",
            "Chowdhury, Bhanwarlal, M.D.": "Chowdhury",
            "Ewing Office, Pft/abi, MD": "Ewing",
            "Gupta, Rajendra, MD": "Gupta",
            "Hamilton Office, Pft/abi, MD": "Hamilton",
            "Huq, U. Irfan, MD": "Huq",
            "Integration, Behavioral Health, MD": "Integration",
            "Khan, Basma, MD": "Khan",
            "Lou, William, MD": "Lou",
            "Management, Chronic Care, MD": "Management_Chronic",
            "Management, Principal Care, MD": "Management_Principal",
            "Matawan Office, Pft/abi, MD": "Matawan",
            "Matthews-brown, R. Spring, MD": "Matthews",
            "Memon, Mushtaq, MD": "Memon",
            "Monitoring, Remote Patient, MD": "Monitoring_Remote_Patient",
            "Monitoring, Remote Therapeutic, MD": "Monitoring_Remote_Therapeutic",
            "Nadeem, Shahzinah, MD": "Nadeem",
            "Raza, Rubina, MD": "Raza",
            "Sheikh, U. Selim, MD": "Sheikh",
            "Taboada, G. Javier, MD": "Taboada",
            "Usmani, H. Qaisar, MD": "Usmani",
            "Younus, W. Mohammad, MD": "Younus",
            "Asiamah-asare, Vida-lynn, NP": "Asiamah",
            "Atieh, Virginia, APN": "Atieh",
            "Brown, Lance, PH": "Brown",
            "Castillo, Kendie, NP/PA": "Castillo",
            "Chavez, Hazel, NP": "Chavez",
            "Dacosta-chambers, Sasha, FNP": "Dacosta",
            "Diaz, Johannelda, NP": "Diaz",
            "Dipietropolo, Lisa, PMHNP-BC": "Dipietropolo",
            "Elshaikh, Barakat": "Elshaikh",
            "Ghafoor, Sadia, DO": "Ghafoor",
            "Huynh-nguyen, P. Anh, NP": "Huynh",
            "Khatri, H. Arti, APN": "Khatri",
            "Management, Chronic Pain, DO": "Management_Chronic",
            "Medical, Azz, DO": "Medical_Azz",
            "Meer, B. Shahid": "Meer_B",
            "Navigator Visit, Suboxone, DO": "Navigator_Visit",
            "Newsome, J. La-toya, NP": "Newsome",
            "Oluwagbamila, Geralda, NP": "Oluwagbamila",
            "Rogers, A. Stephanie, APN": "Rogers",
            "Serzanin, M. Coleen, RN, MSN, Pmhnp-bc": "Serzanin",
            "Viaje, Mabrigida, NP": "Viaje",
        }

        module_name = provider_modules.get(provider_module)
        if module_name:
            module = importlib.import_module(module_name)
        else:
            return {"response": "wrong provider entered"}

        # Dynamically get the task function from the module
        task_function = getattr(module, "task")
        # Call the task function passing the task string
        response = task_function(task, post_date)

        return {"response": response}
    except ModuleNotFoundError:
        raise HTTPException(status_code=404, detail="Module not found")
    except AttributeError:
        raise HTTPException(status_code=500, detail="Task function not found in the module")

@app.post("/history_of_illness")
async def history_of_illness(request: TextGenerationRequest):
    return process_task(request, "Task 1:")
    
@app.post("/plan_of_care")
async def plan_of_care(request: TextGenerationRequest):
    return process_task(request, "Task 2:")

@app.post("/cpt_code")
async def cpt_code(request: TextGenerationRequest):
    return process_task(request, "Task 3:")

@app.post("/physical_exam")
async def physical_exam(request: TextGenerationRequest):
    return process_task(request, "Task 4:")

@app.post("/review_of_system")
async def review_of_system(request: TextGenerationRequest):
    return process_task(request, "Task 5:")
