import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ResultsHistoryGalleryComponent } from './component/results-history-gallery/results-history-gallery.component';
import { FileUploadFormComponent } from './component/file-upload-form/file-upload-form.component';
import { TabsModule } from 'primeng/tabs';
import { FileUploadModule } from 'primeng/fileupload';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, ResultsHistoryGalleryComponent, FileUploadFormComponent, TabsModule, FileUploadModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = '655-final-project-frontend';
}
