import ast
import customtkinter as ctk
from tkinter import messagebox
import math
import datetime

# Configuration de l'apparence
ctk.set_appearance_mode("System")  # Peut être "Light", "Dark" ou "System"
ctk.set_default_color_theme("blue")  # Thèmes disponibles : blue, dark-blue, green

class CalculatriceScientifique(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Calculatrice Scientifique Sécurisée")
        self.geometry("500x700")
        self.minsize(400, 600)
        
        # Variables
        self.historique = []
        self.current_expression = ""
        self.dark_mode = True
        
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.creer_widgets()
        self.bind_events()
        
    def creer_widgets(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Historique
        self.historique_label = ctk.CTkLabel(self.main_frame, text="Historique:", anchor="w")
        self.historique_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        
        self.historique_text = ctk.CTkTextbox(self.main_frame, height=100, state="disabled")
        self.historique_text.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        
        # Affichage
        self.affichage = ctk.CTkEntry(self.main_frame, font=("Arial", 24), justify="right")
        self.affichage.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        # Frame des boutons
        self.boutons_frame = ctk.CTkFrame(self.main_frame)
        self.boutons_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        
        # Boutons scientifiques
        boutons_scientifiques = [
            ('sin', 'sin('), ('cos', 'cos('), ('tan', 'tan('),
            ('π', 'math.pi'), ('e', 'math.e'), ('√', 'math.sqrt('),
            ('^', '**'), ('log', 'math.log10('), ('ln', 'math.log('),
            ('(', '('), (')', ')'), ('abs', 'abs(')
        ]
        
        for i, (text, val) in enumerate(boutons_scientifiques):
            btn = ctk.CTkButton(
                self.boutons_frame, 
                text=text, 
                command=lambda v=val: self.ajouter_expression(v),
                width=60, 
                height=40,
                font=("Arial", 14)
            )
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
        
        # Boutons numériques
        boutons_numeriques = [
            ('7', '7'), ('8', '8'), ('9', '9'), ('/', '/'),
            ('4', '4'), ('5', '5'), ('6', '6'), ('*', '*'),
            ('1', '1'), ('2', '2'), ('3', '3'), ('-', '-'),
            ('0', '0'), ('.', '.'), ('=', ''), ('+', '+')
        ]
        
        for i, (text, val) in enumerate(boutons_numeriques):
            row = 4 + i//4
            col = i%4
            if text == '=':
                btn = ctk.CTkButton(
                    self.boutons_frame, 
                    text=text, 
                    command=self.calculer,
                    width=60, 
                    height=40,
                    fg_color="#2aa44c",
                    hover_color="#1e7e34",
                    font=("Arial", 14, "bold")
                )
            else:
                btn = ctk.CTkButton(
                    self.boutons_frame, 
                    text=text, 
                    command=lambda v=val: self.ajouter_expression(v),
                    width=60, 
                    height=40,
                    font=("Arial", 14)
                )
            btn.grid(row=row, column=col, padx=5, pady=5)
        
        # Boutons de contrôle
        self.control_frame = ctk.CTkFrame(self.main_frame)
        self.control_frame.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ew")
        
        ctk.CTkButton(
            self.control_frame, 
            text="C", 
            command=self.effacer,
            width=60, 
            height=40,
            fg_color="#d9534f",
            hover_color="#c9302c",
            font=("Arial", 14)
        ).grid(row=0, column=0, padx=5, pady=5)
        
        ctk.CTkButton(
            self.control_frame, 
            text="⌫", 
            command=self.effacer_dernier,
            width=60, 
            height=40,
            font=("Arial", 14)
        ).grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkButton(
            self.control_frame, 
            text="☀️/🌙", 
            command=self.changer_theme,
            width=60, 
            height=40,
            font=("Arial", 14)
        ).grid(row=0, column=2, padx=5, pady=5)
        
        ctk.CTkButton(
            self.control_frame, 
            text="?", 
            command=self.afficher_aide,
            width=60, 
            height=40,
            font=("Arial", 14)
        ).grid(row=0, column=3, padx=5, pady=5)
    
    def bind_events(self):
        self.affichage.bind("<Return>", lambda event: self.calculer())
        self.affichage.bind("<Escape>", lambda event: self.effacer())
    
    def ajouter_expression(self, valeur):
        self.current_expression += str(valeur)
        self.affichage.delete(0, "end")
        self.affichage.insert(0, self.current_expression)
    
    def effacer(self):
        self.current_expression = ""
        self.affichage.delete(0, "end")
    
    def effacer_dernier(self):
        self.current_expression = self.current_expression[:-1]
        self.affichage.delete(0, "end")
        self.affichage.insert(0, self.current_expression)
    
    def est_expression_valide(self, expression):
        try:
            arbre = ast.parse(expression, mode='eval')
            
            # Liste des fonctions autorisées
            fonctions_autorisees = {
                'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                'sqrt': math.sqrt, 'log': math.log, 'log10': math.log10,
                'abs': abs, 'pi': math.pi, 'e': math.e
            }
            
            for node in ast.walk(arbre):
                if isinstance(node, ast.Call):
                    if not isinstance(node.func, ast.Name):
                        return False
                    if node.func.id not in fonctions_autorisees:
                        return False
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    return False
                elif isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load):
                    return False
            
            return True
        
        except (SyntaxError, TypeError):
            return False
    
    def calculer(self):
        expression = self.affichage.get()
        
        if not expression:
            return
        
        if not self.est_expression_valide(expression):
            messagebox.showerror("Erreur", "Expression invalide ou dangereuse")
            return
        
        try:
            # Remplace les fonctions mathématiques
            expression = expression.replace("^", "**")
            
            # Évalue l'expression de manière sécurisée
            resultat = eval(expression, {'__builtins__': None}, {
                'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                'sqrt': math.sqrt, 'log': math.log, 'log10': math.log10,
                'abs': abs, 'pi': math.pi, 'e': math.e
            })
            
            # Formatage du résultat
            if isinstance(resultat, float):
                if resultat.is_integer():
                    resultat = int(resultat)
                else:
                    resultat = round(resultat, 10)
            
            # Mise à jour de l'affichage
            self.current_expression = str(resultat)
            self.affichage.delete(0, "end")
            self.affichage.insert(0, self.current_expression)
            
            # Ajout à l'historique
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            self.historique.append(f"{timestamp} : {expression} = {resultat}")
            self.mettre_a_jour_historique()
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de calcul: {str(e)}")
    
    def mettre_a_jour_historique(self):
        self.historique_text.configure(state="normal")
        self.historique_text.delete(1.0, "end")
        self.historique_text.insert("end", "\n".join(self.historique[-5:]))
        self.historique_text.configure(state="disabled")
    
    def changer_theme(self):
        self.dark_mode = not self.dark_mode
        ctk.set_appearance_mode("Dark" if self.dark_mode else "Light")
    
    def afficher_aide(self):
        messagebox.showinfo("Aide",
            "Calculatrice Scientifique Sécurisée\n\n"
            "Fonctions disponibles:\n"
            "- Opérations de base: +, -, *, /, ^ (puissance)\n"
            "- Fonctions trigo: sin(), cos(), tan()\n"
            "- Logarithmes: log() (base 10), ln() (base e)\n"
            "- Constantes: π, e\n"
            "- Autres: sqrt(), abs()\n\n"
            "Sécurité:\n"
            "- Toutes les expressions sont analysées pour\n"
            "  empêcher l'exécution de code dangereux.")

if __name__ == "__main__":
    app = CalculatriceScientifique()
    app.mainloop()