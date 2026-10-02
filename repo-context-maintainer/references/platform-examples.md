# Optional Platform Examples

Read only the section relevant to the repository being closed out. These are
examples, not default requirements.

## Android Application Artifacts

When an authorized workflow includes an APK or Android release artifact:

- verify version name, version code, build variant, source revision, and
  artifact path when available;
- use a traceable file name that follows the repository's convention;
- distinguish build verification from installation or device testing;
- keep release notes focused on user-visible changes, fixes, known issues, and
  verification;
- treat uploading the APK, attaching it to a Release, and publishing the
  Release as separate public actions that each require the applicable approval.
