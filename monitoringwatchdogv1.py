import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import csv
from datetime import datetime

class MyHandler(FileSystemEventHandler):
    def __init__(self, csv_filename):
        self.csv_filename = csv_filename
    
    def on_any_event(self, event):
        if event.is_directory:
            return
        
        if event.event_type == 'created':
            file_path = event.src_path
            creation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # print(f"Event: file created - Path: {file_path}")
            
            self.add_to_csv(file_path, creation_time)
    
    def add_to_csv(self, file_path, creation_time):
        with open(self.csv_filename, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([file_path, creation_time])

if __name__ == "__main__":
    csv_filename = "file_creation_log.csv"
    
    folders_to_watch = [
        #Add the folder path here which we need to monitor
    ]
    
    event_handler = MyHandler(csv_filename)
    
    observers = []
    for folder in folders_to_watch:
        observer = Observer()
        observer.schedule(event_handler, folder, recursive=True)
        observers.append(observer)
    
    for observer in observers:
        observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for observer in observers:
            observer.stop()
    
    for observer in observers:
        observer.join()
