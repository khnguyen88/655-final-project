import { Component, ChangeDetectionStrategy, ChangeDetectorRef, OnDestroy, OnInit } from '@angular/core';
import { MessageService } from 'primeng/api';
import { FileUpload, FileUploadEvent } from 'primeng/fileupload';
import { ToastModule } from 'primeng/toast';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { FormsModule } from '@angular/forms';
import { last, Subscription } from 'rxjs';
import { Router } from '@angular/router';
import { SubmitFormService } from '../../service/submit-form.service';


@Component({
  selector: 'app-file-upload-form',
  imports: [FileUpload, ToastModule, ButtonModule, InputTextModule, FormsModule],
  providers: [MessageService],
  templateUrl: './file-upload-form.component.html',
  styleUrl: './file-upload-form.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class FileUploadFormComponent implements OnInit, OnDestroy{
  subscriptions: Subscription = new Subscription();
  inputUrlValue: string = "";
  acceptedFileExtensions: string[] = ["jpg", "png", "tiff", "gif"];
  isValid: boolean = false;
  
  constructor(private messageService: MessageService, private submitFormService: SubmitFormService, private router: Router, private cd: ChangeDetectorRef) { }

  ngOnInit(): void {
    this.clearForm();
  }

  ngOnDestroy(): void {
    this.subscriptions.unsubscribe();
  }

  onSubmit(urlString: string) {
    alert(urlString);

    if (!this.checkExtension(urlString)) {
      alert("Invalid file, please try another with the correct image extension!");
    }

    this.clearForm();
  }

  clearForm() {
    this.inputUrlValue = "";
  }

  checkExtension(urlString: string) {
    let startOfExtIndex: number = urlString.lastIndexOf(".");
    let urlStringExt: string = urlString.slice(startOfExtIndex);
    alert(urlStringExt);
    return this.acceptedFileExtensions.includes(urlStringExt);
  }

  submitImageUrl(urlString: string) {
    this.subscriptions.add(this.submitFormService.submitForm(urlString).subscribe(
      results => {
        if (results || results.length > 0) {
          alert("Url Path has been successfully submitted");
        }
        else {
          alert("Url Path was not accepted, please try again!")
        }
      }
    ));
  }
}
