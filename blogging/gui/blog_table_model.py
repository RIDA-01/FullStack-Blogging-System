from PyQt6.QtCore import Qt, QAbstractTableModel



class BlogTableModel(QAbstractTableModel):
    def __init__(self, blogs=None):
        super().__init__()
        self.blogs = blogs or []
        self.headers = ['ID', 'Name', 'URL', 'Email']

    def rowCount(self, parent=None):
        return len(self.blogs)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        
        blog = self.blogs[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return str(blog.blog_id)
            elif index.column() == 1:
                return blog.name
            elif index.column() == 2:
                return blog.url
            elif index.column() == 3:
                return blog.email
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]
        return None

    def update_data(self, blogs):
        self.beginResetModel()
        self.blogs = blogs
        self.endResetModel()