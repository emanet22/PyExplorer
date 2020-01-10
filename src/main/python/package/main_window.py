from functools import partial
from PySide2 import QtWidgets, QtCore, QtGui


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.setWindowTitle("PyExplorer")
        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layout()
        self.setup_connections()
        self.create_file_model()
        self.add_actions_to_toolbar()

    def create_widgets(self): #Point1
        self.toolbar = QtWidgets.QToolBar()
        self.tree_view = QtWidgets.QTreeView()
        self.list_view = QtWidgets.QListView()
        self.sld_iconSize = QtWidgets.QSlider() # Slider pour changer la taille des îcones
        self.main_widget = QtWidgets.QWidget()


    def modify_widgets(self):
        # Feuille de style pour améliorer le rendu graphique
        css_file = self.ctx.get_resource("style.css")
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())

        # Changer l'affichage avec des gros îcone
        self.list_view.setViewMode(QtWidgets.QListView.IconMode)

        # Uniformisé la taille de tous les icônes
        self.list_view.setUniformItemSizes(True)
        self.list_view.setIconSize(QtCore.QSize(48, 48))

        self.sld_iconSize.setRange(48, 256)
        self.sld_iconSize.setValue(48)

        # Améliorer la visibilité des icônes
        self.tree_view.setSortingEnabled(True)
        self.tree_view.setAlternatingRowColors(True)

        # Ajuster la taille des colonne au contenu
        self.tree_view.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)


    def create_layouts(self): #Point2
        self.main_laout = QtWidgets.QHBoxLayout(self.main_widget) # Une fenêtre principale qui reprend les widgets (Point3)

    def add_widgets_to_layout(self): #Point3
        # Reprendre les widgets dans la fenêtre centrale
        self.setCentralWidget(self.main_widget)
        # Insérer les widgets dans la fenêtre centrale
        self.main_laout.addWidget(self.tree_view)
        self.main_laout.addWidget(self.list_view)
        self.main_laout.addWidget(self.sld_iconSize)
        # Ajouter la barre outil par défaut en haut (avec module QtCore)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)

    def setup_connections(self):
        self.tree_view.clicked.connect(self.treeview_clicked)
        self.list_view.clicked.connect(self.listview_clicked)
        self.list_view.doubleClicked.connect(self.listview_double_clicked)
        #self.sld_iconSize.ValueChanged.connect(self.change_icon_size)

    def change_icon_size(self, value):
        self.list_view.setIconSize(QtCore.QSize(Value, Value))
        # Value = récupère la valeur du slide (test possible avec un print(value))


    def create_file_model(self):
        # Création du modèle
        self.model = QtWidgets.QFileSystemModel()
        # Configurer le chemin par défaut indépendant du système OS, tous les modifications seront reconnus
        root_path = QtCore.QDir.rootPath()
        self.model.setRootPath(root_path)
        self.tree_view.setModel(self.model)
        self.list_view.setModel(self.model)

        # Root index, là ou notre vue va commencer
        self.tree_view.setRootIndex(self.model.index(root_path))
        self.list_view.setRootIndex(self.model.index(root_path))

    def treeview_clicked(self, index):
        #Index retourne des informations sur le dossier sur lequel on a cliqué
        if self.model.isDir(index): #Dans cette condition c'est un dossier > On affiche le contenu du dossier
            self.list_view.setRootIndex(index)
        else: #Dans cette condition c'est un fichier > O affiche donc le dossier parent
            self.list_view.setRootIndex(index.parent())

    def listview_clicked (self, index):
        #Simple click, synchronise la navigation dans la fenêtre de gauche
        selection_model = self.tree_view.selectionModel()
        selection_model.setCurrentIndex(index, QtCore.QItemSelectionModel.ClearAndSelect)

    def listview_double_clicked(self, index):
        #Double click, ouvre le dossier dans la fenêtre de gauche
        self.tree_view.setRootIndex(index)

    def add_actions_to_toolbar(self):
        # Lien documentation: https://doc.qt.io/qtforpython/PySide2/QtCore/QStandardPaths.html
        #Création des icônes basé sur des fichiers svg
        locations = ["home", "desktop", "documents", "music", "movies", "pictures"] #Même nom en minuscule que les icônes .svg
        for location in locations:
            icon = self.ctx.get_resource(f"{location}.svg") #Va chercher dans le dossier /resources/base
            action = self.toolbar.addAction(QtGui.QIcon(icon), location.capitalize()) #Capitalize met une majuscule au début du mot > Home (nom qui sera affiché si on passe la souris dessus)
            action.triggered.connect(partial(self.change_location, location))

    def change_location(self, location):
        #Détournement de contactenage pour déterminer le lien des dossiers
        standard_path = QtCore.QStandardPaths()
        path = eval(f"standard_path.standardLocations(QtCore.QStandardPaths.{location.capitalize()}Location)")
        path = path[0] #Prend le premier élement Expl.: D:/em007/Videos au lieu de ['D:/em007/Videos']
        self.tree_view.setRootIndex(self.model.index(path))
        self.list_view.setRootIndex(self.model.index(path))





