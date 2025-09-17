{{- define "demo-chart.name" -}}demo-app{{- end -}}
{{- define "demo-chart.fullname" -}}{{ include "demo-chart.name" . }}{{- end -}}
