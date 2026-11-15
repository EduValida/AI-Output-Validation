import json

def atualizar(dados, dict):
    
    for item in dados:
        
        competencia_output = str(item.get("competencia", ""))

        for tup in dict:

            competencia_dict = str(tup.get("competencia", ""))
            completion_threshold = int(tup.get("completion threshold", ""))

            if competencia_output == competencia_dict:
                nivel = int(item.get("nivel"))
                if nivel >= completion_threshold:
                    item["status"] = 1
                else:
                    item["status"] = 0

    return dados