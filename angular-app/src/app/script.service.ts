import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { Observable, map } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ScriptService {
  baseUrl = 'http://localhost:5000/api/';
  constructor(private http: HttpClient, private sanitizer: DomSanitizer) {}

  callScript(apiEndpoint: string, country: string): Observable<SafeUrl[]> {
    return this.http
      .post<{ success: boolean; images: string[] }>(
        this.baseUrl + apiEndpoint,
        { country }
      )
      .pipe(
        map((response) => {
          if (response.success) {
            return response.images.map((image) =>
              this.sanitizer.bypassSecurityTrustUrl(
                `data:image/png;base64,${image}`
              )
            );
          } else {
            console.error('Error running script');
            return [];
          }
        })
      );
  }
}
