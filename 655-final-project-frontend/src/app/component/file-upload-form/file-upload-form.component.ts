import { Component } from '@angular/core';
import { MessageService } from 'primeng/api';
import { FileUpload, FileUploadEvent } from 'primeng/fileupload';
import { ToastModule } from 'primeng/toast';
import { ButtonModule } from 'primeng/button';

interface UploadEvent {
    originalEvent: Event;
    files: File[];
}

@Component({
  selector: 'app-file-upload-form',
  imports: [FileUpload, ToastModule, ButtonModule],
  providers: [MessageService],
  templateUrl: './file-upload-form.component.html',
  styleUrl: './file-upload-form.component.scss'
})

export class FileUploadFormComponent {
  urlPath: string = 'https://final-project-655-put-image-into-storage-bucket-770833528905.us-central1.run.app'
  
  constructor(private messageService: MessageService) {}

  onUpload(event: FileUploadEvent) {
    alert(JSON.stringify(event));
    this.messageService.add({ severity: 'info', summary: 'Success', detail: 'File Uploaded with Basic Mode' });
  }
}
