import os
import csv
import json

class FileManager:
    #Task 1: FileManager
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print("Checking file...")
        if os.path.exists(self.filename):
            print(f"File found: {self.filename}")
            return True
        else:
            print(f"Error: File '{self.filename}' not found.")
            return False

    def create_output_folder(self, folder_name="output"):
        print("Checking output folder....")
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f"Output folder created: {folder_name}/")
        else:
            print(f"Output folder already exists: {folder_name}/")

class DataLoader:
    #Task 2: DataLoader
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        print("Loading data...")
        try:
            with open(self.filename, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.students = list(reader)
            print(f"Data loaded successfully: {len(self.students)} students")
        except Exception as e:
            print(f"Error loading CSV: {e}")

    def preview(self, n=5):
        print(f"First {n} rows:")
        print("-" * 30)
        for s in self.students[:n]:
            print(
                f"{s.get('student_id')} | {s.get('age')} | {s.get('gender')} | {s.get('country')} GPA: {s.get('GPA')}")
        print("-" * 30)


class DataAnalyser:
    #Task 3: DataAnalyser
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        low_sleep_gpas = []
        high_sleep_gpas = []

        for s in self.students:
            try:
                gpa = float(s['GPA'])
                sleep = float(s['sleep_hours'])

                if sleep < 6:
                    low_sleep_gpas.append(gpa)
                else:
                    high_sleep_gpas.append(gpa)
            except (ValueError, KeyError):
                continue

        avg_low = sum(low_sleep_gpas) / len(low_sleep_gpas) if low_sleep_gpas else 0
        avg_high = sum(high_sleep_gpas) / len(high_sleep_gpas) if high_sleep_gpas else 0

        self.result = {
            "analysis": "Sleep vs GPA",
            "low_cnt": len(low_sleep_gpas),
            "high_cnt": len(high_sleep_gpas),
            "low_avg_gpa": round(avg_low, 2),
            "high_avg_gpa": round(avg_high, 2),
            "difference": round(avg_high - avg_low, 2)
        }

    def print_results(self):
        print("Sleep vs GPA Analysis")
        print("-" * 30)
        print(f"Students sleeping < 6 hours: {self.result['low_cnt']} avg GPA: {self.result['low_avg_gpa']}")
        print(f"Students sleeping >= 6 hours: {self.result['high_cnt']} avg GPA: {self.result['high_avg_gpa']}")
        print(f"GPA Difference: {self.result['difference']}")
        print("-" * 30)


class ResultSaver:
    #Task 4: ResultSaver
    def __init__(self, data, output_path):
        self.data = data
        self.output_path = output_path

    def save_json(self):
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4)
            print(f"Result saved to {self.output_path}")
        except Exception as e:
            print(f"Error saving JSON: {e}")


if __name__ == "__main__":
    # Task 5: Main
    fm = FileManager('students.csv')
    if not fm.check_file():
        print('Stopping program.')
        exit()
    fm.create_output_folder()

    dl = DataLoader('students.csv')
    dl.load()
    dl.preview()

    analyser = DataAnalyser(dl.students)
    analyser.analyse()
    analyser.print_results()

    saver = ResultSaver(analyser.result, 'output/result.json')
    saver.save_json()