results = model.train(
    data=yaml_file_path,
    epochs=100,            
    imgsz=640,
    patience=20,           
    batch=32,             
    optimizer='AdamW',      
    lr0=0.001,             
    lrf=0.2,               
    dropout=0.0            
)
post_training_files_path ='/kaggle/working/ultralytics/runs/detect/train432'
best_model_path = os.path.join(post_training_files_path, 'weights/best.pt')

best_model = YOLO(best_model_path)

metrics = best_model.val(split='val')
