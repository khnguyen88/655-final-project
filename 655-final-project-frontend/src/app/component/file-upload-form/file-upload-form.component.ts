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
import { CustomFormData } from '../../interfaces/model';


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
    const formData: CustomFormData = {
      urlString: urlString
    }

    if (!this.checkExtension(urlString)) {
      alert("Invalid file, please try another with the correct image extension!");
    }
    else {
      this.submitImageUrl(formData);
    }

    this.clearForm();
  }

  clearForm() {
    this.inputUrlValue = "";
  }

  checkExtension(urlString: string) {
    let startOfExtIndex: number = urlString.lastIndexOf(".");
    if (startOfExtIndex == -1 || startOfExtIndex == urlString.length) {
      return false;
    }
    let urlStringExt: string = urlString.slice(startOfExtIndex + 1);
    return this.acceptedFileExtensions.includes(urlStringExt);
  }

  submitImageUrl(formData: CustomFormData) {
    this.subscriptions.add(this.submitFormService.submitForm(formData).subscribe(
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
