import json

class Ramo:
    #codigo = ""
    #nombre = ""
    #creditos = 0
    #requisitos = []
    #equivalencias = []
    #cursos = []

    def __init__(self, soup_ramo):
        # Nombre y código
        title_components = soup_ramo.find("h2").getText().split("\n")[1].lstrip().split(" ")
        self.codigo = title_components[0]
        self.nombre = " ".join(title_components[1:])

        # Leyenda details
        self.equivalencias = ""
        self.requisitos = ""
        self.creditos = 0

        soup_details = soup_ramo.find("div", class_="accordion")
        soup_leyenda = soup_details.find("dl", class_="leyenda")
        soup_leyenda_dt = soup_leyenda.find_all("dt")
        soup_leyenda_dd = soup_leyenda.find_all("dd")

        for i in range(len(soup_leyenda_dt)):
            detail_type = soup_leyenda_dt[i].getText()
            detail_content = soup_leyenda_dd[i].getText()

            if detail_type == "Créditos":
                self.creditos = int(detail_content)
            elif detail_type == "Requisitos":
                self.requisitos = detail_content        # todo: This needs to be parsed properly
            elif detail_type == "Equivalencias":        # todo: CC6908,(EI4205/EI2090),CC5402 -> abstract syntax tree
                self.equivalencias = detail_content     # todo: This needs to be parsed properly too

        # Curso details
        self.cursos = []
        soup_cursos = soup_details.find("table", class_="cursos").find("tbody").find_all("tr")
        for soup_curso in soup_cursos:
            self.cursos.append(Curso(soup_curso))

    def __repr__(self):
        return f"{self.codigo} {self.nombre}"

    def cursos_to_json(self):
        cursos_jsons = []
        for curso in self.cursos:
            cursos_jsons.append(curso.to_json())
        return cursos_jsons

    def to_json(self):
        return {
                "codigo": self.codigo,
                "nombre": self.nombre,
                "numero_cursos": len(self.cursos),
                "cursos": self.cursos_to_json(),
                "creditos": self.creditos,
                "requsitos": self.requisitos,
                "equivalencias": self.equivalencias
                }


class Curso:
    def __init__(self, soup_curso):
        self.nombre = soup_curso.find("h1").getText().strip()

        # Profesores
        self.profesores = []
        soup_profes = soup_curso.find("ul", class_="profes").find_all("li")
        for soup_profe in soup_profes:
            profe = soup_profe.find("h1")
            self.profesores.append(profe.getText().strip())

        # Column data
        soup_columns = soup_curso.find_all("td")
        self.cupos = soup_columns[1].getText().strip()
        self.ocupados = soup_columns[2].getText().strip()
        self.horario = soup_columns[3].getText().strip()  # todo: parse this

    def to_json(self):
        return {
                "nombre": self.nombre,
                "profesores": self.profesores,
                "cupos": self.cupos,
                "ocupados": self.ocupados,
                "horario": self.horario
                }
