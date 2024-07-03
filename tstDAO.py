from database.DAO import DAO
from model.modello import Model

res = DAO.getAllObjects()
model = Model()

conn = DAO.getAllConnessioni(model._idMap)

print(len(res))
print(len(conn))
