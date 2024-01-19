from EmpDb import EmpDb
from EmpGuiTk import EmpGuiTk

def main():
    db = EmpDb(init=False, dbName='EmpDb.csv')
    app = EmpGuiTk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()