package kubernetes.validating.images

deny[msg] {
  input.request.kind.kind == "Pod"
  image := input.request.object.spec.containers[_].image
  not startswith(image, "my-company-registry/")
  msg := sprintf("Image '%v' comes from an untrusted registry", [image])
}
