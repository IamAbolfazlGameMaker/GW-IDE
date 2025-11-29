# --- File: core/file_manager.py ---

from PySide6.QtWidgets import QTreeView, QFileSystemModel
from PySide6.QtCore import Signal, QDir, QModelIndex # Import QModelIndex for type hinting
# ... other imports ...

# Define Debug function (copied from your snippet for completeness)
logger = "0"
try:
    from addons.debug import *
    print("Debug module loaded!")
    logger = "1"
except ModuleNotFoundError:
    print("Debug module NOT found. Defaulting to normal printing")

def Debug(val):
    if logger == "1":
        log(val)
    else:
        print(val)
# ------------------------------------

class FileManager(QTreeView):
    file_open_requested = Signal(str)

    def __init__(self):
        super().__init__()
        self.model = QFileSystemModel()
        
        default_path = QDir.currentPath()
        self.model.setRootPath(default_path)
        
        self.setModel(self.model)
        self.setRootIndex(self.model.index(default_path))
        
        self.doubleClicked.connect(self.on_double_click)
        
        for i in range(1, self.model.columnCount()):
            self.setColumnHidden(i, True)
            
        self.setColumnWidth(0, 300) 
        self.setHeaderHidden(True)

    def on_double_click(self, index):
        if self.model.isDir(index):
            return
        
        file_path = self.model.filePath(index)
        self.file_open_requested.emit(file_path)

    def set_root_path(self, path):
        if QDir(path).exists():
            self.model.setRootPath(path)
            self.setRootIndex(self.model.index(path))
            return True
        else:
            Debug(f"Error: Directory not found: {path}")
            return False

    # ✅ CORRECTION 3: ADDING THE MISSING refresh_view METHOD
    def refresh_view(self):

        current_root_path = self.model.rootPath()
        root_index = self.model.index(current_root_path)
    
    # 1. Ask the model to reload the contents of the root index.
    # This is the correct PySide/Qt way to manually trigger an update 
    # of the directory listing if auto-monitoring is delayed or missed.
        self.model.setRootPath(current_root_path)
    
    # 2. Tell the view to re-display the contents starting from the root index.
        self.setRootIndex(root_index)
    
    # 3. Force the view to repaint itself to guarantee the change is visible.
        self.viewport().update()
    
        Debug("DEBUG: FileManager view updated via model reload.")